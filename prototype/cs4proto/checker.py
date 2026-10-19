"""Proof checker: DataMatrix decode, OCR, value comparison, required elements per market from the graph,
and symbol template matching. Deterministic rules decide; low-confidence results are routed to review."""
import difflib
import re
import unicodedata

import cv2
import numpy as np
import zxingcpp

from .model import (MARKETS, PHRASES, REQ_BY_ID, SYMBOLS, gtin_valid, in_rel, out_rel, required_reqs)
from .render import draw_symbol

SYMBOL_THRESHOLD = 0.70   # TM_CCOEFF_NORMED score needed to accept a symbol detection
TEXT_THRESHOLD = 0.80     # fuzzy-match ratio needed to accept an OCR text match
OCR_REVIEW_SCORE = 0.80   # OCR lines below this confidence are routed to human review
# Symbols that are editions of the same concept: they compete, and the pinned edition must win.
FAMILIES = {"sym:ec_rep_2021": "ec_rep", "sym:ec_rep_a1": "ec_rep"}
# Which catalogue requirement a failed check cites, per check (intersected with the element's links).
CHECK_CLAUSES = {
    "hri_match": {"US-801.40", "EU-VI-C4.1"},
    "carrier": {"US-801.20", "EU-23.2(h)"},
    "date_format": {"US-801.18"},
}

_ocr = None


def ocr_engine():
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    return _ocr


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)).casefold())


def fuzzy_find(expected, text):
    """Best similarity of `expected` to any same-length window of `text` (both normalised)."""
    e, t = norm(expected), text
    if not e:
        return 1.0
    if e in t:
        return 1.0
    best = 0.0
    for i in range(0, max(1, len(t) - len(e) + 1)):
        best = max(best, difflib.SequenceMatcher(None, e, t[i:i + len(e)]).ratio())
    return best


def parse_gs1(text):
    """Parse a bracketed GS1 element string for AIs 01, 17, 10, 21."""
    s = unicodedata.normalize("NFKC", text).replace(" ", "")
    pats = {"01": r"\(0[1lI]\)(\d{14})", "17": r"\(17\)(\d{6})", "10": r"\(10\)([A-Za-z0-9]{1,20})",
            "21": r"\(21\)([A-Za-z0-9]{1,20})"}
    out = {ai: (m.group(1) if (m := re.search(p, s)) else None) for ai, p in pats.items()}
    return out if all(out.values()) else None


def match_symbols(gray):
    """Score every synthetic symbol template against the proof. Returns sid -> (score, bbox)."""
    out = {}
    for sid in SYMBOLS:
        tpl = np.asarray(draw_symbol(sid))
        best = (-1.0, None)
        for s in (0.95, 1.0, 1.05):
            t = cv2.resize(tpl, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
            res = cv2.matchTemplate(gray, t, cv2.TM_CCOEFF_NORMED)
            _, mx, _, loc = cv2.minMaxLoc(res)
            if mx > best[0]:
                best = (mx, (loc[0], loc[1], loc[0] + t.shape[1], loc[1] + t.shape[0]))
        out[sid] = best
    return out


def clauses(G, element, check=None):
    reqs = [r.split(":", 1)[1] for r in out_rel(G, element, "REQUIRED_BY")] if element in G else []
    if check:
        reqs = [r for r in reqs if r in CHECK_CLAUSES[check]]
    return [(r, G.nodes[f"req:{r}"]["clause"]) for r in reqs]


def finding(code, severity, element, cl, message, bbox=None, evidence=None):
    return {"code": code, "severity": severity, "element": element, "clauses": cl, "message": message,
            "bbox": bbox, "evidence": evidence or {}}


def check_proof(G, artwork, image):
    """Check one proof image against what the graph says this label must carry."""
    a = G.nodes[artwork]
    label, market, level, lang = a["label"], a["market"], a["level"], a["lang"]
    jur = MARKETS[market][0]
    product = {k.split(":", 1)[1]: G.nodes[k]["value"] for k, d in G.nodes(data=True) if d["type"] == "attribute"}
    typed = {"sterile": product["sterile"] == "True", "single_use": product["single_use"] == "True",
             "rx": product["rx"] == "True", "manufacturer_country": product["manufacturer_country"]}
    el = lambda kind: f"el:{label}:{kind}"
    gray = np.asarray(image.convert("L"))
    F, trace = [], {}

    # 1. DataMatrix decode (AIDC).
    codes = [b for b in zxingcpp.read_barcodes(gray) if b.format == zxingcpp.BarcodeFormat.DataMatrix]
    dm = parse_gs1(codes[0].text) if codes else None
    trace["datamatrix"] = {"decoded": codes[0].text if codes else None,
                           "symbology": codes[0].symbology_identifier if codes else None}
    if not dm:
        F.append(finding("AIDC_UNREADABLE", "major", "udi_carrier", clauses(G, el("udi_carrier"), "carrier"),
                         "No GS1 DataMatrix could be decoded"))
    else:
        if codes[0].content_type != zxingcpp.ContentType.GS1:
            F.append(finding("AIDC_NOT_GS1", "major", "udi_carrier", clauses(G, el("udi_carrier"), "carrier"),
                             f"DataMatrix content is not GS1 ({codes[0].content_type})"))
        if not gtin_valid(dm["01"]):
            F.append(finding("GTIN_CHECK_DIGIT", "major", "udi_carrier", clauses(G, el("udi_carrier"), "carrier"),
                             f"GTIN {dm['01']} fails the check digit"))
        expected = {"01": product[f"gtin_{level}"], "10": product["lot"], "21": product[f"serial_{level}"],
                    "17": product["expiry"][2:4] + product["expiry"][5:7] + product["expiry"][8:10]}
        for ai, want in expected.items():
            if dm[ai] != want:
                F.append(finding("AIDC_VS_SOURCE", "major", "udi_carrier", clauses(G, el("udi_carrier"), "carrier"),
                                 f"AIDC ({ai}) = {dm[ai]} but product data says {want}"))

    # 2. OCR the whole proof, with the decoded barcode area blanked so its modules are not read as text.
    ocr_img = gray.copy()
    for b in codes:
        p = b.position
        xs = [p.top_left.x, p.top_right.x, p.bottom_left.x, p.bottom_right.x]
        ys = [p.top_left.y, p.top_right.y, p.bottom_left.y, p.bottom_right.y]
        ocr_img[max(0, min(ys) - 10):max(ys) + 10, max(0, min(xs) - 10):max(xs) + 10] = 255
    lines, _ = ocr_engine()(ocr_img)
    lines = sorted(lines or [], key=lambda r: (round(r[0][0][1] / 20), r[0][0][0]))
    full = norm(" ".join(t for _, t, _ in lines))
    lines = [(b, unicodedata.normalize("NFKC", t), sc) for b, t, sc in lines]
    trace["ocr_lines"] = [(t, round(s, 3)) for _, t, s in lines]
    low = [t for _, t, s in lines if s < OCR_REVIEW_SCORE]
    if low:
        F.append(finding("OCR_LOW_CONFIDENCE", "review", "-", [], f"{len(low)} OCR line(s) below confidence "
                         f"{OCR_REVIEW_SCORE}; routed to human review", evidence={"lines": low}))

    # 3. HRI vs AIDC, field by field (dates compared by value).
    hri = parse_gs1("|".join(t for _, t, _ in lines))  # '|' stops a value at the end of its OCR line
    trace["hri"] = hri
    hri_tokens = [(b, t) for b, t, _ in lines if "(" in t]
    hri_box = None
    if hri_tokens:
        pts = np.array([p for b, _ in hri_tokens for p in b])
        hri_box = (int(pts[:, 0].min()), int(pts[:, 1].min()), int(pts[:, 0].max()), int(pts[:, 1].max()))
    if not hri:
        F.append(finding("HRI_UNREADABLE", "review", "udi_carrier", clauses(G, el("udi_carrier"), "hri_match"),
                         "Human-readable UDI not found or not parseable by OCR; human review", hri_box))
    elif dm:
        for ai in ("01", "17", "10", "21"):
            if hri[ai] != dm[ai]:
                F.append(finding("HRI_AIDC_MISMATCH", "major", "udi_carrier", clauses(G, el("udi_carrier"), "hri_match"),
                                 f"HRI ({ai}) = {hri[ai]} but DataMatrix ({ai}) = {dm[ai]}", hri_box,
                                 {"hri": hri[ai], "aidc": dm[ai]}))

    # 4. Symbols: detect, then check presence and pinned edition.
    scores = match_symbols(gray)
    trace["symbol_scores"] = {k: round(v[0], 3) for k, v in scores.items()}
    found = {sid for sid, (s, _) in scores.items() if s >= SYMBOL_THRESHOLD}
    for fam in set(FAMILIES.values()):  # keep only the best-scoring edition in a family
        members = [s for s in found if FAMILIES.get(s) == fam]
        for s in sorted(members, key=lambda s: scores[s][0])[:-1]:
            found.discard(s)

    # 5. Required elements for this market and level, derived from the requirement catalogue.
    reqs = required_reqs(typed, market, level)
    req_kinds = {}
    for r in reqs:
        req_kinds.setdefault(r.kind, []).append((r.rid, r.clause))
    trace["required"] = {k: [c for _, c in v] for k, v in req_kinds.items()}

    def pinned_symbol(kind):
        syms = [s for s in out_rel(G, el(kind), "RENDERED_AS") if s.startswith("sym:")] if el(kind) in G else []
        return syms[0] if syms else None

    def text_present(expected):
        return fuzzy_find(expected, full) >= TEXT_THRESHOLD

    def text_right_of(box):
        """OCR lines that start right of a symbol and sit on the same row."""
        if box is None:
            return []
        x1, y1, x2, y2 = box
        return [(b, t) for b, t, _ in lines
                if b[0][0] >= x2 - 5 and b[0][0] < x2 + 200 and y1 - 10 <= (b[0][1] + b[2][1]) / 2 <= y2 + 10]

    dates = re.findall(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)", " ".join(t for _, t, _ in lines))

    for kind, cl in req_kinds.items():
        if kind == "udi_carrier":
            continue  # covered by steps 1 and 3
        pin = pinned_symbol(kind)
        phrase = PHRASES.get(kind, {}).get(lang if kind != "rx_only" else "EN")
        if kind == "quantity":
            phrase = phrase.format(n=product["pack_quantity"])
        if kind in ("manufacturer", "auth_rep"):
            phrase = product[kind].split(",")[0]
        sym_ok = pin is None or pin in found
        family_hit = None
        if pin in FAMILIES:
            family_hit = next((s for s in found if FAMILIES.get(s) == FAMILIES[pin]), None)
        txt_ok = phrase is None or text_present(phrase)
        if kind == "lot":
            near = text_right_of(scores["sym:lot"][1] if "sym:lot" in found else None)
            txt_ok = bool(near)
            if near and dm and norm(near[0][1]) != norm(dm["10"]):
                b = near[0][0]
                F.append(finding("LOT_FIELD_VS_AIDC", "major", "lot", cl,
                                 f"LOT field reads {near[0][1]} but DataMatrix (10) = {dm['10']}",
                                 (int(b[0][0]), int(b[0][1]), int(b[2][0]), int(b[2][1]))))
        if kind == "use_by":
            txt_ok = bool(dates)

        if family_hit and family_hit != pin:
            F.append(finding("SYMBOL_OUTDATED", "major", kind,
                             sorted(set(cl + [("EU-23.1(h)", REQ_BY_ID["EU-23.1(h)"].clause)])),
                             f"{SYMBOLS[family_hit][0]} placeholder for {SYMBOLS[family_hit][1]} found; "
                             f"graph pins {SYMBOLS[pin][1]}", scores[family_hit][1],
                             {"found": family_hit, "pinned": pin, "score": round(scores[family_hit][0], 3)}))
        elif kind == "md" and not sym_ok and txt_ok:
            F.append(finding("ARTWORK_DEVIATION", "minor", kind, [],
                             "MD symbol missing but the text indication is present; 23.2(q) is met, the "
                             "approved artwork is not"))
        elif not sym_ok and not txt_ok or (pin is None and not txt_ok):
            F.append(finding("REQUIRED_ELEMENT_MISSING", "major", kind, cl,
                             f"Required element '{kind}' not found on the proof"))
        elif not sym_ok:
            F.append(finding("SYMBOL_MISSING", "major", kind, cl, f"Symbol for '{kind}' not found; text present"))
        elif not txt_ok:
            F.append(finding("TEXT_MISSING", "major", kind, cl, f"Text for '{kind}' not found; symbol present"))

    # 6. Value checks on printed fields.
    if jur == "US" and "use_by" in req_kinds and not dates:
        F.append(finding("DATE_FORMAT", "major", "use_by", clauses(G, el("use_by"), "date_format"),
                         "No YYYY-MM-DD date found on a US label"))
    if dm and dates:
        y, m, d = dates[0]
        if f"{y[2:]}{m}{d}" != dm["17"]:
            F.append(finding("DATE_VS_AIDC", "major", "use_by", req_kinds.get("use_by", []),
                             f"Printed use-by {y}-{m}-{d} differs from AIDC (17) {dm['17']}"))

    # 7. Elements on the artwork with no verified requirement link (traceability gap, not a defect).
    for e in in_rel(G, artwork, "PLACED_ON"):
        if not out_rel(G, e, "REQUIRED_BY"):
            F.append(finding("UNLINKED_ELEMENT", "info", G.nodes[e]["kind"], [],
                             "Element has no verified requirement link in the catalogue (e.g. MDR Art. 20 "
                             "was not verified in research)"))
    return F, trace
