"""Render SYNTHETIC label proofs with Pillow: placeholder symbols, real GS1 DataMatrix, two-line HRI."""
import io
import random
from pathlib import Path

import numpy as np
import zxingcpp
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .model import PHRASES, PRODUCT, MARKETS, udi_fields

FONT_DIR = Path("C:/Windows/Fonts")
SYM_W, SYM_H = 110, 70


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:  # non-Windows fallback
        return ImageFont.load_default(size)


def _sym_canvas():
    im = Image.new("L", (SYM_W, SYM_H), 255)
    return im, ImageDraw.Draw(im)


def _tag(d):
    d.text((SYM_W - 26, SYM_H - 12), "SYN", font=font(9), fill=0)


def draw_symbol(sid):
    """Synthetic placeholder glyphs. They are NOT the ISO 15223-1 graphics."""
    im, d = _sym_canvas()
    if sid == "sym:manufacturer":  # filled factory silhouette
        d.polygon([(10, 60), (10, 30), (35, 15), (35, 30), (60, 15), (60, 30), (85, 15), (85, 60)], fill=0)
    elif sid == "sym:ec_rep_2021":
        d.rectangle([4, 12, 104, 56], outline=0, width=3)
        d.line([40, 12, 40, 56], fill=0, width=3)
        d.text((9, 22), "EC", font=font(22, True), fill=0)
        d.text((46, 22), "REP", font=font(22, True), fill=0)
    elif sid == "sym:ec_rep_a1":  # placeholder for the Amd 1 glyph (real glyph not verified)
        d.rectangle([4, 8, 104, 60], outline=0, width=3)
        d.rectangle([10, 14, 98, 54], outline=0, width=2)
        d.text((22, 20), "REP", font=font(24, True), fill=0)
        d.text((80, 38), "A1", font=font(12, True), fill=0)
    elif sid == "sym:lot":
        d.rectangle([10, 14, 100, 56], outline=0, width=3)
        d.text((26, 20), "LOT", font=font(24, True), fill=0)
    elif sid == "sym:use_by":  # hourglass
        d.polygon([(30, 8), (80, 8), (55, 35)], outline=0, fill=None, width=3)
        d.polygon([(55, 35), (30, 62), (80, 62)], fill=0)
    elif sid == "sym:sterile_eo":
        d.rectangle([2, 14, 106, 56], outline=0, width=3)
        d.line([76, 14, 76, 56], fill=0, width=3)
        d.text((7, 25), "STERILE", font=font(15, True), fill=0)
        d.text((80, 24), "EO", font=font(18, True), fill=0)
    elif sid == "sym:do_not_reuse":
        d.ellipse([30, 8, 84, 62], outline=0, width=3)
        d.text((47, 16), "2", font=font(30, True), fill=0)
        d.line([34, 58, 80, 12], fill=0, width=4)
    elif sid == "sym:md":
        d.rectangle([20, 12, 92, 58], outline=0, width=3)
        d.text((32, 18), "MD", font=font(28, True), fill=0)
    elif sid == "sym:ce":
        d.text((14, 12), "CE", font=font(38, True), fill=0)
    else:
        raise KeyError(sid)
    _tag(d)
    return im


def datamatrix(fields, scale=8):
    content = f"(01){fields['01']}(17){fields['17']}(10){fields['10']}(21){fields['21']}"
    bc = zxingcpp.create_barcode(content, zxingcpp.BarcodeFormat.DataMatrix, gs1=True, force_square=True)  # square GS1 DataMatrix
    return Image.fromarray(np.array(bc.to_image(scale=scale))).convert("L")


def hri_lines(fields):
    return [f"(01) {fields['01']} (17) {fields['17']}", f"(10) {fields['10']} (21) {fields['21']}"]


def render_label(market, level, symbol_for, product=PRODUCT, defects=None):
    """symbol_for: element kind -> symbol id (read from the graph). defects: seeded proof defects."""
    defects = defects or {}
    omit = set(defects.get("omit", []))
    symbol_for = {**symbol_for, **defects.get("symbol_override", {})}
    jur, lang = MARKETS[market]
    W, H = 1200, 780
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    layout = {}

    d.rectangle([0, 0, W, 36], fill=60)
    d.text((14, 7), "SYNTHETIC DEMO LABEL  -  NOT A REAL DEVICE  -  NOT FOR CLINICAL USE", font=font(20, True), fill=255)
    d.text((30, 50), product["name"], font=font(30, True), fill=0)
    d.text((30, 88), f"Model {product['model']}   |   {market} {level} label   |   {lang}", font=font(18), fill=0)
    if "device_name" not in omit:
        d.text((30, 116), PHRASES["device_name"][lang], font=font(22), fill=0)
        layout["device_name"] = (30, 116, 700, 145)

    rows = {"left": 160, "right": 160}
    kinds_left = ["manufacturer", "auth_rep", "lot", "use_by"]
    kinds_right = ["sterile", "single_use", "md", "ce_mark", "rx_only", "quantity"]
    from .model import label_kinds
    present = [k for k in label_kinds(market, level) if k not in omit]

    def row(col, kind, lines, sym=True):
        x = 30 if col == "left" else 640
        y = rows[col]
        if sym and kind in symbol_for:
            im.paste(draw_symbol(symbol_for[kind]), (x, y))
            layout[f"sym:{kind}"] = (x, y, x + SYM_W, y + SYM_H)
        tx = x + SYM_W + 14 if sym else x
        for i, (t, f) in enumerate(lines):
            d.text((tx, y + 8 + i * 28), t, font=f, fill=0)
        layout[kind] = (x, y, x + 540, y + SYM_H)
        rows[col] += SYM_H + 16

    mname, maddr = product["manufacturer"].split(", ", 1)
    rname, raddr = product["auth_rep"].split(", ", 1)
    expiry = product["expiry"].isoformat()  # YYYY-MM-DD (21 CFR 801.18; also year+month for 23.2(i))
    content = {
        "manufacturer": [(mname, font(19, True)), (maddr, font(18))],
        "auth_rep": [(rname, font(19, True)), (raddr, font(18))],
        "lot": [(defects.get("lot_field", product["lot"]), font(26, True))],
        "use_by": [(expiry, font(26, True)), (PHRASES["use_by"][lang], font(16))],
        "sterile": [(PHRASES["sterile"][lang], font(19))],
        "single_use": [(PHRASES["single_use"][lang], font(19))],
        "md": [(PHRASES["md"][lang], font(19))],
        "ce_mark": [(product["notified_body"], font(26, True))],
        "rx_only": [(PHRASES["rx_only"]["EN"], font(30, True))],
        "quantity": [(PHRASES["quantity"][lang].format(n=product["pack_quantity"]), font(22, True))],
    }
    for kind in kinds_left + kinds_right:
        if kind in present:
            row("left" if kind in kinds_left else "right", kind, content[kind], sym=kind != "rx_only" and kind != "quantity")

    fields = udi_fields(product, level)
    dm = datamatrix(fields)
    y0 = 548
    im.paste(dm, (30, y0))
    layout["datamatrix"] = (30, y0, 30 + dm.width, y0 + dm.height)
    hri_fields = {**fields, **defects.get("hri", {})}
    for i, line in enumerate(hri_lines(hri_fields)):
        d.text((30 + dm.width + 30, y0 + 30 + i * 40), line, font=font(24), fill=0)
    layout["hri"] = (30 + dm.width + 30, y0 + 25, W - 20, y0 + 115)
    d.text((30, H - 26), "Symbols are synthetic placeholders, not ISO 15223-1 artwork. UDI data are fictional.",
           font=font(14), fill=90)
    return im, layout


def degrade(im, seed=0):
    """Approximate a scanned print proof: slight blur, sensor noise, JPEG compression."""
    rng = np.random.default_rng(seed)
    im = im.filter(ImageFilter.GaussianBlur(0.7))
    a = np.asarray(im, dtype=np.float32) + rng.normal(0, 6, (im.height, im.width))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=70)
    return Image.open(io.BytesIO(buf.getvalue())).convert("L")
