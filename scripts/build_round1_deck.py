"""Build the Case Study 4 Round 1 deck from the Teliport S4 template.

Usage: python CS4/scripts/build_round1_deck.py <pptx-skill-dir> [out.pptx]

Slides: 1 cover, 2 solution one-pager, 3 Annexure A (process map), 4 Annexure B (automation opportunity
matrix and impact model), 5 Annexure C (prototype). Same approach as CS1/scripts/build_round1_deck.py:
template XML edited in place, native shapes, connectors and tables, minimum 10 pt. Screenshots come from
CS4/prototype/outputs and are cropped and compressed before embedding. Numbers are read from
CS4/notes/impact_model.json and CS4/prototype/outputs/scenario3_findings.json so the slides match them.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image

CS4 = Path(__file__).resolve().parents[1]
TEMPLATE = CS4.parent / "case_studies" / "Teliport S4_Submission Template.pptx"
DEFAULT_OUT = CS4 / "submission" / "Tejaswi_Innovex_Indian Institute of Information Technology Kottayam_CS4.pptx"
SCREENS = CS4 / "prototype" / "outputs" / "screens"
IMPACT = json.loads((CS4 / "notes" / "impact_model.json").read_text(encoding="utf-8"))
RUNS = json.loads((CS4 / "prototype" / "outputs" / "scenario3_findings.json").read_text(encoding="utf-8"))

EMU = 914400
NAVY, BLUE, SKY, TINT, GRID = "0B2545", "0077B6", "D9EEF9", "F1F7FB", "C9D6E2"
ACCENT, MUTED, WHITE, RED, GREEN, PURPLE = "E07A00", "4A5A6A", "FFFFFF", "C62828", "2E7D32", "5E35B1"
MODE = {"A": ("Automated", BLUE), "AH": ("AI-assisted", ACCENT), "H": ("Human", PURPLE)}
EMPTY_PARA = '<a:p><a:endParaRPr lang="en-US" sz="1000" dirty="0"/></a:p>'  # a txBody needs >= 1 paragraph
REL_IMAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"


def e(inches):
    return int(round(inches * EMU))


def fmt_h(v):
    return f"{v:g}"


class Slide:
    """Accumulates shape XML for one slide with unique ids."""

    def __init__(self):
        self.parts, self.next_id = [], 100

    def _id(self):
        self.next_id += 1
        return self.next_id

    def box(self, name, x, y, w, h, paras, fill=None, line=None, geom="rect", anchor="t",
            inset=(0.06, 0.04, 0.06, 0.04), radius=None, line_w=0.75):
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
        line_xml = (f'<a:ln w="{int(line_w * 12700)}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
                    if line else "<a:ln><a:noFill/></a:ln>")
        av = f'<a:gd name="adj" fmla="val {radius}"/>' if radius is not None else ""
        l, t, r, b = (e(v) for v in inset)
        self.parts.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{self._id()}" name="{escape(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}"><a:avLst>{av}</a:avLst></a:prstGeom>{fill_xml}{line_xml}</p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" anchor="{anchor}" rtlCol="0">'
            f'<a:noAutofit/></a:bodyPr><a:lstStyle/>'
            f'{"".join(para_xml(p) for p in paras) or EMPTY_PARA}</p:txBody></p:sp>')

    def arrow(self, name, x1, y1, x2, y2, color=BLUE, w_pt=1.5, dashed=False):
        flip = (' flipH="1"' if x2 < x1 else "") + (' flipV="1"' if y2 < y1 else "")
        dash = '<a:prstDash val="dash"/>' if dashed else ""
        self.parts.append(
            f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{self._id()}" name="{escape(name)}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
            f'<p:spPr><a:xfrm{flip}><a:off x="{e(min(x1, x2))}" y="{e(min(y1, y2))}"/>'
            f'<a:ext cx="{e(abs(x2 - x1))}" cy="{e(abs(y2 - y1))}"/></a:xfrm>'
            f'<a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>'
            f'<a:ln w="{int(w_pt * 12700)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{dash}'
            f'<a:tailEnd type="triangle" w="med" len="med"/></a:ln></p:spPr></p:cxnSp>')

    def pic(self, name, rid, x, y, w, h, line=GRID):
        self.parts.append(
            f'<p:pic><p:nvPicPr><p:cNvPr id="{self._id()}" name="{escape(name)}" descr="{escape(name)}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:ln w="6350"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln></p:spPr></p:pic>')

    def table(self, name, x, y, col_w, rows, header_fill=NAVY, row_h=0.3, fills=None, mar=0.07, heights=None):
        """rows[0] is the header. Each cell is a str or a list of paragraphs. fills: {(r, c): hex}."""
        fills = fills or {}
        heights = heights or [row_h] * len(rows)
        grid = "".join(f'<a:gridCol w="{e(w)}"/>' for w in col_w)
        trs = []
        for ri, row in enumerate(rows):
            tcs = []
            for ci, cell in enumerate(row):
                paras = cell if isinstance(cell, list) else [P(cell, sz=10, b=ri == 0, color=WHITE if ri == 0 else NAVY)]
                fill = header_fill if ri == 0 else fills.get((ri, ci), WHITE if ri % 2 else TINT)
                border = "".join(f'<a:{s} w="6350"><a:solidFill><a:srgbClr val="{GRID}"/></a:solidFill></a:{s}>'
                                 for s in ("lnL", "lnR", "lnT", "lnB"))
                tcs.append(f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>{"".join(para_xml(p) for p in paras)}</a:txBody>'
                           f'<a:tcPr marL="{e(mar)}" marR="{e(mar)}" marT="{e(0.025)}" marB="{e(0.025)}" anchor="ctr">'
                           f'{border}<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill></a:tcPr></a:tc>')
            trs.append(f'<a:tr h="{e(heights[ri])}">{"".join(tcs)}</a:tr>')
        self.parts.append(
            f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{self._id()}" name="{escape(name)}"/>'
            f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
            f'<p:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(sum(col_w))}" cy="{e(sum(heights))}"/></p:xfrm>'
            f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
            f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/><a:tblGrid>{grid}</a:tblGrid>{"".join(trs)}</a:tbl>'
            f'</a:graphicData></a:graphic></p:graphicFrame>')

    def xml(self):
        return "".join(self.parts)


def P(*runs, sz=11, b=False, i=False, color=NAVY, algn="l", bullet=False, after=0, **_):
    """A paragraph. Runs are str or (str, {sz,b,i,color}) tuples; paragraph-level style is the default."""
    norm = [(r, {}) if isinstance(r, str) else r for r in runs]
    return {"runs": [(t, {"sz": sz, "b": b, "i": i, "color": color, **o}) for t, o in norm],
            "algn": algn, "bullet": bullet, "after": after}


BANNED = ("—", "seamless", "robust", "leverage", "empower", "cutting-edge")


def para_xml(p):
    assert all(o["sz"] >= 10 for _, o in p["runs"]), "font below 10 pt"
    for t, _ in p["runs"]:
        assert not any(w in t.lower() for w in BANNED), f"banned word or em dash in: {t}"
    bu = ('<a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>' if p["bullet"] else "<a:buNone/>")
    ind = ' marL="128016" indent="-128016"' if p["bullet"] else ' marL="0" indent="0"'
    spc = f'<a:spcAft><a:spcPts val="{int(p["after"] * 100)}"/></a:spcAft>' if p["after"] else ""
    runs = "".join(
        f'<a:r><a:rPr lang="en-US" sz="{int(o["sz"] * 100)}" b="{int(o["b"])}" i="{int(o["i"])}" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{o["color"]}"/></a:solidFill><a:latin typeface="Calibri"/><a:cs typeface="Calibri"/></a:rPr>'
        f'<a:t xml:space="preserve">{escape(t)}</a:t></a:r>' for t, o in p["runs"])
    return f'<a:p><a:pPr algn="{p["algn"]}"{ind}>{spc}{bu}</a:pPr>{runs}</a:p>'


def title_xml(main, sub, y=0.9, h=0.5):
    return (f'<p:spPr><a:xfrm><a:off x="{e(0.4)}" y="{e(y)}"/><a:ext cx="{e(12.53)}" cy="{e(h)}"/></a:xfrm></p:spPr>'
            f'<p:txBody><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
            + para_xml(P((main, {"sz": 24, "b": True, "color": BLUE}), (sub, {"sz": 16, "color": NAVY})))
            + "</p:txBody>")


def set_title_and_drop_body(xml, main, sub):
    start = xml.index('<p:ph type="title"/>')
    sppr = xml.index("<p:spPr>", start)
    end = xml.index("</p:sp>", sppr)
    xml = xml[:sppr] + title_xml(main, sub) + xml[end:]
    ph = xml.index('<p:ph idx="1"/>')
    s = xml.rindex("<p:sp>", 0, ph)
    t = xml.index("</p:sp>", ph) + len("</p:sp>")
    return xml[:s] + xml[t:]


def append_shapes(xml, shapes):
    return xml.replace("</p:spTree>", shapes + "</p:spTree>", 1)


class Media:
    """Crops and compresses screenshots into the package and registers slide relationships."""

    def __init__(self, work):
        self.work, self.n = work, 0

    def add(self, slide_name, src, crop, fmt):
        self.n += 1
        name = f"cs4_screen{self.n}.{'jpeg' if fmt == 'JPEG' else 'png'}"
        im = Image.open(src).convert("RGB").crop(crop)
        dst = self.work / "ppt" / "media" / name
        if fmt == "JPEG":
            im.save(dst, "JPEG", quality=82, optimize=True)
        else:
            im.quantize(colors=64, method=Image.Quantize.MEDIANCUT).save(dst, "PNG", optimize=True)
        rels = self.work / "ppt" / "slides" / "_rels" / f"{slide_name}.rels"
        x = rels.read_text(encoding="utf-8")
        rid = f"rId{100 + self.n}"
        x = x.replace("</Relationships>",
                      f'<Relationship Id="{rid}" Type="{REL_IMAGE}" Target="../media/{name}"/></Relationships>')
        rels.write_text(x, encoding="utf-8")
        return rid, im.size


# --------------------------------------------------------------------------- slide 1: cover
def build_cover(xml, media):
    xml = xml.replace("<a:t>Case Study No.  </a:t>", "<a:t>Case Study No. 4</a:t>")
    sub = "".join(para_xml(p) for p in [
        P("Team Innovex", sz=18, b=True, algn="ctr"),
        P("Tejaswi Jaddu (Team Leader) · Bichu Devnarayan", sz=14, algn="ctr"),
        P("Indian Institute of Information Technology Kottayam", sz=14, algn="ctr"),
    ])
    empty = '<a:p><a:endParaRPr lang="en-US" dirty="0"/></a:p></p:txBody></p:sp></p:spTree>'
    assert xml.count(empty) == 1
    return xml.replace(empty, sub + "</p:txBody></p:sp></p:spTree>")


# --------------------------------------------------------------------------- slide 2: one-pager
COVERAGE = [  # p.5 pain points x modules (cs4_design.md §9). 2 = primary, 1 = supporting.
    ("1. Time-Consuming Manual Process", {"M0": 1, "M1": 2, "M3": 2, "M4": 2, "M5": 1, "WF": 1}),
    ("2. Frequent Regulatory Updates", {"M0": 1, "M1": 2, "M2": 2}),
    ("3. Symbol Management", {"M0": 2, "M1": 1, "M2": 1, "M3": 2, "M4": 2}),
    ("4. Multiple Sources of Truth", {"M0": 2}),
    ("5. Expertise Dependency", {"M0": 2, "M2": 1, "M3": 2, "M5": 1, "M6": 1}),
    ("6. Manual Redlining", {"M1": 1, "M4": 2, "M5": 2}),
    ("7. Repetitive Review", {"M3": 2, "M4": 2, "WF": 1}),
    ("8. Traceability", {"M0": 2, "M1": 1, "WF": 2}),
    ("9. Variant Explosion", {"M0": 2, "M1": 2, "M5": 2}),
    ("10. Human Error", {"M0": 1, "M3": 2, "M4": 2, "M5": 2, "M6": 1}),
]
MODS = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "WF"]


def seeded_summary():
    seeded = [r for r in RUNS if not r["proof"].startswith("ctrl")]
    caught = sum(len(r["caught"]) for r in seeded)
    expected = sum(len(r["expected"]) for r in seeded)
    false = sum(len(r["false_flags"]) for r in RUNS)
    review = sum(len(r["review_flags"]) for r in RUNS)
    return caught, expected, false, len(RUNS), review


def impact_range():
    c = IMPACT["cases"]
    lo, hi = c["pessimistic (both sides)"], c["base"]
    return lo, hi


def build_main(xml, media):
    xml = set_title_and_drop_body(xml, "ClauseLink", ": every label element traced to the clause that requires it")
    s = Slide()
    top, body_top, body_bot = 1.5, 1.85, 5.55
    LX, LW, CX, CW, RX, RW = 0.4, 3.45, 4.0, 4.95, 9.1, 3.83

    def header(x, w, text):
        s.box(f"Header {text}", x, top, w, 0.3, [P(text, sz=13, b=True, color=BLUE)], inset=(0, 0, 0, 0), anchor="b")

    header(LX, LW, "The problem")
    header(CX, CW, "Architecture: the graph is the system of record")
    header(RX, RW, "Coverage of the 10 pain points (p.5)")

    # ---- left: problem
    s.box("Scale", LX, body_top, LW, 0.36, [
        P("A single product change may require updates to ", ("30+ labels", {"b": True}), " and ",
          ("20+ languages", {"b": True}), " (p.4).", sz=10),
    ], inset=(0, 0, 0, 0))
    s.box("Error causes", LX, body_top + 0.41, LW, 1.52, [
        P("Causes of human error named in the case study (p.4):", sz=10, b=True, after=1),
        P("Manual data entry and copying between ERP, PLM, labelling software and regulatory databases",
          sz=10, bullet=True),
        P("Requirements that keep changing: UDI updates, new symbols, MDR changes", sz=10, bullet=True),
        P("Reviewers comparing old versions, new versions and regulatory documents by hand", sz=10, bullet=True),
        P("Translation inconsistencies; visual inspection that depends on people", sz=10, bullet=True),
    ], inset=(0, 0, 0, 0))
    cy = body_top + 1.99
    s.box("Recall card", LX, cy, LW, body_bot - cy, [], fill=TINT, geom="roundRect", radius=6000)
    s.box("Recall title", LX + 0.1, cy + 0.05, LW - 0.2, 0.22,
          [P("FDA device recall records with a labeling root cause", sz=10, b=True)], inset=(0, 0, 0, 0))
    stats = [("5.59%", "of 59,481 records, all years", 0.22), ("3.95%", "of 10,299 records, 2021 to 2025", 0.22),
             ("135 of 407", "2021 to 2025 labeling records cite \"Labeling Change Control\"", 0.34)]
    y = cy + 0.31
    for k, (num, lab, h) in enumerate(stats):
        s.box(f"Recall stat {k}", LX + 0.1, y, 0.98, h, [P(num, sz=13, b=True, color=BLUE)],
              inset=(0, 0, 0, 0), anchor="ctr")
        s.box(f"Recall label {k}", LX + 1.1, y, LW - 1.2, h, [P(lab, sz=10)], inset=(0, 0, 0, 0), anchor="ctr")
        y += h + 0.03
    s.box("Recall source", LX + 0.1, y + 0.02, LW - 0.2, body_bot - y - 0.04, [
        P("Source: openFDA device recall API, five labeling root-cause categories, data as of 2026-10-15. "
          "Records are per product; openFDA says to treat them as unvalidated.", sz=10, color=MUTED),
    ], inset=(0, 0, 0, 0))

    # ---- centre: architecture
    s.box("Inputs", CX, body_top, CW, 0.28, [
        P(("Inputs: ", {"b": True}), "PLM and ERP data, regulatory sources, existing approved labels",
          sz=10, color=WHITE, algn="ctr")], fill=NAVY, geom="roundRect", radius=20000, anchor="ctr",
          inset=(0.05, 0, 0.05, 0))
    mw, gw = 1.45, 1.81
    gx = CX + (CW - gw) / 2
    gy, gh = body_top + 0.42, 2.12
    s.box("Graph", gx, gy, gw, gh, [], fill=SKY, line=BLUE, geom="roundRect", radius=8000, line_w=1.5)
    s.box("Graph title", gx, gy + 0.05, gw, 0.22, [P("M0 Knowledge graph", sz=11, b=True, algn="ctr")],
          inset=(0, 0, 0, 0))
    chain = [("Requirement", "the clause that requires it"), ("Label element", "LOT, UDI, warning, symbol"),
             ("Source data", "PLM or ERP attribute"), ("Artwork", "market, language, level"),
             ("Approval", "change order, e-signature")]
    ph, pg, p0 = 0.32, 0.04, gy + 0.3
    s.box("Chain spine", gx + gw / 2 - 0.015, p0 + ph / 2, 0.03, 4 * (ph + pg), [], fill=BLUE)
    for k, (t, sub) in enumerate(chain):
        s.box(f"Chain {t}", gx + 0.08, p0 + k * (ph + pg), gw - 0.16, ph,
              [P(t, sz=10, b=True, algn="ctr"), P(sub, sz=10, color=MUTED, algn="ctr")],
              fill=WHITE, line=GRID, geom="roundRect", radius=16000, anchor="ctr", inset=(0.02, 0, 0.02, 0))
    s.arrow("Inputs to graph", gx + gw / 2, body_top + 0.29, gx + gw / 2, gy - 0.01, color=NAVY)

    def module(tag, title, text, x, y, h, w=mw):
        s.box(f"Module {tag}", x, y, w, h, [
            P((f"{tag} ", {"color": BLUE}), title, sz=10.5, b=True, after=1),
            P(text, sz=10, color=MUTED),
        ], fill=WHITE, line=BLUE, geom="roundRect", radius=10000, inset=(0.07, 0.04, 0.05, 0.03))
        return x, y, w, h

    mh = (gh - 0.11) / 2
    side = [module("M2", "Regulatory intelligence", "Cited rule changes; RA approves them.", CX, gy, mh),
            module("M5", "Authoring and translation", "Approved phrases only; new text is a draft.",
                   CX, gy + mh + 0.11, mh),
            module("M1", "Change-impact engine", "One query to every affected label.", CX + CW - mw, gy, mh),
            module("M6", "UDI-DI change detector", "MDR Annex VI 3.9 triggers; US cases go to RA.",
                   CX + CW - mw, gy + mh + 0.11, mh)]
    for x, y, w, h in side:
        my = y + h / 2
        if x < gx:
            s.arrow("Module link", x + w + 0.03, my, gx - 0.03, my, color=BLUE)
        else:
            s.arrow("Module link", gx + gw + 0.03, my, x - 0.03, my, color=BLUE)

    by, bh = gy + gh + 0.11, 0.76
    bw = (CW - 0.36) / 3
    module("M3", "Compliance checker", "Rules decide; LLM notes are flagged.", CX, by, bh, w=bw)
    module("M4", "CV verification", "Printed UDI vs DataMatrix, symbols.", CX + bw + 0.18, by, bh, w=bw)
    gate_x = CX + 2 * (bw + 0.18)
    s.box("Gate", gate_x, by, bw, bh, [
        P("Human e-signature gate", sz=10.5, b=True, color=WHITE, after=1),
        P("RA and QA sign; AI never approves.", sz=10, color=WHITE),
    ], fill=ACCENT, geom="roundRect", radius=10000, inset=(0.07, 0.04, 0.05, 0.03))
    s.arrow("Graph to checks", gx + gw / 2, gy + gh + 0.01, gx + gw / 2, by - 0.01, color=BLUE)
    s.arrow("Check to verify", CX + bw + 0.02, by + bh / 2, CX + bw + 0.16, by + bh / 2, color=NAVY)
    s.arrow("Verify to gate", gate_x - 0.16, by + bh / 2, gate_x - 0.02, by + bh / 2, color=NAVY)
    ry = by + bh + 0.04
    s.box("Release", CX, ry, CW, body_bot - ry, [
        P(("Release: ", {"b": True}), "signed version, change order and audit trail written back to the graph",
          sz=10, algn="ctr")], fill=TINT, line=GRID, geom="roundRect", radius=30000, anchor="ctr",
          inset=(0.05, 0, 0.05, 0))

    # ---- right: coverage grid, drawn with shapes so row heights are exact
    cell_w, hdr_h = 0.24, 0.26
    name_w = RW - cell_w * len(MODS)
    s.box("Grid header", RX, body_top, RW, hdr_h, [P("Pain point", sz=10, b=True, color=WHITE)], fill=NAVY,
          anchor="ctr", inset=(0.05, 0, 0, 0))
    for k, m in enumerate(MODS):
        s.box(f"Grid col {m}", RX + name_w + k * cell_w, body_top, cell_w, hdr_h,
              [P(m, sz=10, b=True, color=WHITE, algn="ctr")], anchor="ctr", inset=(0, 0, 0, 0))
    y = body_top + hdr_h
    for ri, (name, cov) in enumerate(COVERAGE):
        h = 0.36 if len(name) >= 30 else 0.27
        fill = TINT if ri % 2 else WHITE
        s.box(f"Grid row {ri + 1}", RX, y, RW, h, [P(name, sz=10)], fill=fill, line=GRID, anchor="ctr",
              inset=(0.05, 0, cell_w * len(MODS) + 0.03, 0), line_w=0.5)
        for k, m in enumerate(MODS):
            cx = RX + name_w + k * cell_w
            if k == 0:
                s.box("Grid divider", cx, y, 0.005, h, [], fill=GRID)
            lvl = cov.get(m)
            if lvl:
                d = 0.12
                s.box(f"Dot {ri + 1} {m}", cx + (cell_w - d) / 2, y + (h - d) / 2, d, d, [],
                      fill=BLUE if lvl == 2 else WHITE, line=BLUE, geom="ellipse", line_w=1.25)
        y += h
    s.box("Coverage legend", RX, y + 0.06, RW, body_bot - y - 0.06, [
        P(("●", {"color": BLUE}), " primary   ", ("○", {"color": BLUE}), " supporting.  M0 graph, M1 to M6 "
          "modules, WF workflow with e-signature and audit trail. Every pain point has a primary module.",
          sz=10, color=MUTED),
    ], inset=(0, 0, 0, 0))

    # ---- bottom strip
    sy, sh = 5.72, 1.56
    panels = [(0.4, 4.75), (5.3, 3.55), (9.0, 3.93)]
    for k, (x, w) in enumerate(panels):
        s.box(f"Strip panel {k}", x, sy, w, sh, [], fill=TINT, geom="roundRect", radius=6000)

    x, w = panels[0]
    rid, (iw, ih) = media.add("slide2.xml", SCREENS / "2_annotated_label.png", (25, 95, 1580, 760), "JPEG")
    ph_ = 1.12
    pw = ph_ * iw / ih
    s.pic("Prototype proof (synthetic)", rid, x + 0.1, sy + (sh - ph_) / 2, pw, ph_)
    caught, expected, false, nproofs, review = seeded_summary()
    s.box("Prototype caption", x + pw + 0.2, sy + 0.1, w - pw - 0.28, sh - 0.2, [
        P("Prototype check", sz=10.5, b=True, after=2),
        P(f"Synthetic test: {caught}/{expected} seeded defects caught, {false} false flags across {nproofs} proofs; "
          "uncertain reads go to a human.", sz=10, after=2),
        P("Shown: printed lot differs from the DataMatrix.", sz=10, color=MUTED),
    ], inset=(0, 0, 0, 0))

    x, w = panels[1]
    lo, hi = impact_range()
    s.box("Flow and effort", x + 0.14, sy + 0.1, w - 0.28, sh - 0.16, [
        P("Process coverage", sz=10.5, b=True, after=2),
        P("18-step flow plus a change trigger: 8 automated, 7 AI-assisted, 4 human (stakeholder review and "
          "3 approvals).", sz=10, after=3),
        P(("Estimate: ", {"b": True, "color": ACCENT}),
          f"{lo['saved_pct']:.1f}% to {hi['saved_pct']:.1f}% less manual effort per change "
          f"({fmt_h(lo['saved_h'])} to {fmt_h(hi['saved_h'])} h saved) for the 30-label, 20-language example. "
          "Assumptions in Annexure B.", sz=10),
    ], inset=(0, 0, 0, 0))

    x, w = panels[2]
    s.box("Guardrails", x + 0.14, sy + 0.1, w - 0.28, sh - 0.16, [
        P("Guardrails", sz=10.5, b=True, after=2),
        P(("AI never approves. ", {"b": True}), "RA and QA e-sign every release.", sz=10, bullet=True),
        P(("Part 11 audit trail: ", {"b": True}), "time-stamped record of every change (21 CFR 11.10(e)).",
          sz=10, bullet=True),
        P(("Risk-based review: ", {"b": True}), "full review for UDI, warnings and sterile data.", sz=10, bullet=True),
        P(("Validated ", {"b": True}), "as quality-system software (QMSR / ISO 13485, FDA CSA 2026).",
          sz=10, bullet=True),
    ], inset=(0, 0, 0, 0))
    return append_shapes(xml, s.xml())


# --------------------------------------------------------------------------- slide 3: Annex A
PROCESS = [  # (step, today (PDF verbatim), with ClauseLink, mode, module) from cs4_design.md §1.3
    ("0", "(new) Change trigger", "PLM/ERP change, approved rule change or new market opens a change record", "A", "M0, M2"),
    ("1", "Product / Design Information", "Connectors sync product attributes with source ID and version", "A", "M0"),
    ("2", "Product Understanding", "Attributes that drive requirements shown with their source; extracted values "
     "need owner confirmation", "AH", "M0"),
    ("3", "Identify Applicable Markets", "Read from registration and ERP data; RA confirms any new market", "AH", "M0"),
    ("4", "Regulatory Requirement Assessment", "Graph query returns the applicable clauses; new rules enter only after "
     "RA approval", "AH", "M0, M2"),
    ("5", "Gap Assessment", "Rule diff of required vs present elements, per label, market and level", "A", "M3"),
    ("6", "Identify Labeling Gaps", "Gap list with clause citations", "A", "M3"),
    ("7", "Gap Addressal", "Content proposed from the approved phrase library; the engineer accepts or edits", "AH", "M5"),
    ("8", "Label Content Development", "Label assembled from graph elements, no copy and paste", "AH", "M5"),
    ("9", "Redline / Artwork Modification", "Redline generated from the graph diff; layout changes proposed", "AH",
     "M5, M4"),
    ("10", "Stakeholder Review", "Risk-ranked packet: changed elements with clause, source and check results", "H", "WF"),
    ("11", "Regulatory / Quality Approval", "Part 11 e-signature; AI never approves", "H", "WF"),
    ("12", "Label Revision", "New version committed to the graph and linked to the approval", "A", "M0"),
    ("13", "Change Order Creation", "Drafted with the full impacted list; a person releases it", "A", "M1, WF"),
    ("14", "Document / Configuration Control", "The versioned graph is the configuration record, synced to PLM", "A", "M0"),
    ("15", "Final Quality Check", "CV checks the print proof; QA reviews every flag and signs", "AH", "M4, WF"),
    ("16", "Label Release", "E-signed release", "H", "WF"),
    ("17", "Manufacturing", "Released files go to the existing print system; CV checks samples", "A", "M4"),
    ("18", "Production Implementation", "Line clearance and first-article sign-off with CV evidence", "H", "WF"),
]


def build_annex_a(xml, media):
    xml = set_title_and_drop_body(xml, "Annexure A", ": Supporting detail, process map today and with ClauseLink")
    s = Slide()
    counts = {m: sum(1 for r in PROCESS if r[3] == m) for m in MODE}
    assert counts == {"A": 8, "AH": 7, "H": 4}, counts
    hdr = ["#", "Today (case study, p.3)", "With ClauseLink", "Mode", "Module"]
    table = [[[P(h, sz=10, b=True, color=WHITE)] for h in hdr]]
    for n, today, new, mode, mod in PROCESS:
        label, col = MODE[mode]
        table.append([[P(n, sz=10, b=True)], [P(today, sz=10, b=True, i=n == "0")], [P(new, sz=10)],
                      [P(label, sz=10, b=True, color=col)], [P(mod, sz=10)]])
    row_h = 0.262
    s.table("Process map", 0.4, 1.5, [0.4, 2.75, 7.08, 1.2, 1.1], table, row_h=row_h)
    ny = 1.5 + row_h * 20 + 0.12
    s.box("Process note", 0.4, ny, 12.53, 7.3 - ny, [
        P(("Count: ", {"b": True, "color": BLUE}),
          f"{counts['A']} automated, {counts['AH']} AI-assisted with a human check, {counts['H']} human, over the 18 "
          "steps plus the new change trigger. Steps 4 and 9 mix automated and AI-assisted work and are counted as "
          "AI-assisted. Stakeholder review and the three approvals (11, 16, 18) stay human.", sz=10.5),
    ], fill=TINT, geom="roundRect", radius=8000, anchor="ctr", inset=(0.15, 0.04, 0.15, 0.04))
    return append_shapes(xml, s.xml())


# --------------------------------------------------------------------------- slide 4: Annex B
AOM = [  # (step, effort, error risk, automation potential, module) from cs4_design.md §2, team estimates
    ("1", "Product / Design Information", 2, 3, 3, "M0"), ("2", "Product Understanding", 2, 2, 2, "M0"),
    ("3", "Identify Applicable Markets", 1, 2, 2, "M0"), ("4", "Regulatory Requirement Assessment", 3, 3, 2, "M0, M2"),
    ("5", "Gap Assessment", 3, 3, 3, "M3"), ("6", "Identify Labeling Gaps", 2, 3, 3, "M1, M3"),
    ("7", "Gap Addressal", 2, 2, 2, "M5"), ("8", "Label Content Development", 3, 3, 2, "M5"),
    ("9", "Redline / Artwork Modification", 3, 2, 3, "M5, M4"), ("10", "Stakeholder Review", 3, 2, 2, "WF, M3"),
    ("11", "Regulatory / Quality Approval", 2, 2, 1, "WF"), ("12", "Label Revision", 1, 2, 3, "M0"),
    ("13", "Change Order Creation", 2, 2, 3, "M1"), ("14", "Document / Configuration Control", 2, 2, 3, "M0"),
    ("15", "Final Quality Check", 3, 3, 3, "M4"), ("16", "Label Release", 1, 2, 1, "WF"),
    ("17", "Manufacturing", 2, 3, 2, "M4"), ("18", "Production Implementation", 2, 2, 1, "WF"),
]


def build_annex_b(xml, media):
    xml = set_title_and_drop_body(xml, "Annexure B",
                                  ": Supporting detail, automation opportunity matrix and impact model")
    s = Slide()
    hdr = ["#", "Step", "Effort", "Error risk", "Automation", "Priority", "Module"]
    table = [[[P(h, sz=10, b=True, color=WHITE, algn="l" if k < 2 or k == 6 else "ctr")] for k, h in enumerate(hdr)]]
    fills = {}
    for ri, (n, step, ef, er, au, mod) in enumerate(AOM, 1):
        pr = ef + er + au
        if pr == 9:
            fills.update({(ri, c): "FDEBD3" for c in range(7)})
        table.append([[P(n, sz=10, b=True)], [P(step, sz=10)]] +
                     [[P(str(v), sz=10, algn="ctr")] for v in (ef, er, au)] +
                     [[P(str(pr), sz=10, b=True, color=ACCENT if pr == 9 else NAVY, algn="ctr")], [P(mod, sz=10)]])
    row_h = 0.262
    s.table("Automation opportunity matrix", 0.4, 1.5, [0.38, 2.62, 0.62, 0.78, 0.9, 0.7, 0.8], table, row_h=row_h,
            fills=fills)
    ny = 1.5 + row_h * 19 + 0.1
    s.box("AOM note", 0.4, ny, 6.8, 7.3 - ny, [
        P("Scores 1 (low) to 3 (high) are team estimates from the p.5 pain points, not measurements. Priority is "
          "the sum (maximum 9). Steps 5 and 15 score highest.", sz=10, color=MUTED),
    ], inset=(0, 0, 0, 0))

    # ---- impact model
    X, Wd = 7.45, 5.48
    s.box("Impact header", X, 1.5, Wd, 0.3, [P("Impact model: one change, 30 labels × 20 languages (estimate)",
                                                sz=12, b=True, color=BLUE)], inset=(0, 0, 0, 0), anchor="b")
    a = IMPACT["assumptions"]
    tb, tp = a["today"]["base"], a["today"]["pessimistic"]
    pb, pp = a["platform"]["base"], a["platform"]["pessimistic"]
    rows = [["Assumption", "Base", "Pessimistic"],
            ["Today: impact assessment", f"{fmt_h(tb['impact_h'])} h", f"{fmt_h(tp['impact_h'])} h"],
            ["Today: redline per label", f"{fmt_h(tb['redline_h'])} h", f"{fmt_h(tp['redline_h'])} h"],
            ["Today: review per language block", f"{tb['block_min']} min × {tb['reviewers']} reviewers",
             f"{tp['block_min']} min × {tp['reviewers']} reviewers"],
            ["Today: final check per label", f"{fmt_h(tb['qc_h'])} h", f"{fmt_h(tp['qc_h'])} h"],
            ["ClauseLink: RA confirms impact list", f"{fmt_h(pb['confirm_h'])} h", f"{fmt_h(pp['confirm_h'])} h"],
            ["ClauseLink: layout check per label", f"{fmt_h(pb['layout_h'])} h", f"{fmt_h(pp['layout_h'])} h"],
            ["ClauseLink: diff-only packet per label", f"{pb['packet_min']} min × {pb['packet_reviewers']}",
             f"{pp['packet_min']} min × {pp['packet_reviewers']}"],
            ["ClauseLink: flagged blocks reviewed", f"{round(pb['flag_rate'] * 100)}% at {pb['block_min_flag']} min",
             f"{round(pp['flag_rate'] * 100)}% at {pp['block_min_flag']} min"],
            ["ClauseLink: QA review of CV evidence", f"{fmt_h(pb['qc_evidence_h'])} h per label",
             f"{fmt_h(pp['qc_evidence_h'])} h per label"]]
    s.table("Impact assumptions", X, 1.9, [2.78, 1.35, 1.35], rows, row_h=0.262)
    cases = IMPACT["cases"]
    res = [["Case", "Today", "ClauseLink", "Saved"]]
    for name, label in [("base", "Base"), ("pessimistic platform only", "Pessimistic ClauseLink side"),
                        ("pessimistic (both sides)", "Pessimistic on both sides")]:
        c = cases[name]
        res.append([label, f"{fmt_h(c['today_h'])} h", f"{fmt_h(c['platform_h'])} h",
                    [P(f"{fmt_h(c['saved_h'])} h ({c['saved_pct']:.1f}%)", sz=10, b=True, color=ACCENT)]])
    ry = 1.9 + 0.262 * 10 + 0.2
    s.table("Impact results", X, ry, [2.18, 0.95, 1.05, 1.3], res, row_h=0.28)
    ny = ry + 0.28 * 4 + 0.12
    s.box("Impact notes", X, ny, Wd, 7.3 - ny, [
        P(f"Every label is assumed to carry all 20 languages: {a['blocks']} language blocks. Effort only. Elapsed "
          "time depends on approval queues and is not claimed; error rates and real timings come from a pilot "
          "audit trail.", sz=10, color=MUTED),
    ], inset=(0, 0, 0, 0))
    return append_shapes(xml, s.xml())


# --------------------------------------------------------------------------- slide 5: Annex C
PLAIN = {"HRI_AIDC_MISMATCH": "Printed UDI differs from DataMatrix", "REQUIRED_ELEMENT_MISSING": "Required element missing",
         "SYMBOL_OUTDATED": "Symbol edition outdated"}


def build_annex_c(xml, media):
    xml = set_title_and_drop_body(xml, "Annexure C", ": Supporting detail, prototype on synthetic data")
    s = Slide()
    rid, (iw, ih) = media.add("slide5.xml", SCREENS / "1_graph_impact.png", (0, 110, 1600, 900), "PNG")
    pw = 7.25
    ph = pw * ih / iw
    s.box("Graph caption", 0.4, 1.5, pw, 0.3, [P("Scenario 1: ISO 15223-1 Amd 1 changes the EC REP symbol; one graph "
                                                  "query finds the 4 affected labels", sz=11, b=True, color=BLUE)],
          inset=(0, 0, 0, 0), anchor="b")
    s.pic("Graph impact view (synthetic)", rid, 0.4, 1.85, pw, ph)

    X, Wd = 7.9, 5.03
    s.box("Findings header", X, 1.5, Wd, 0.3, [P("Scenario 3: seeded-defect proofs", sz=11, b=True, color=BLUE)],
          inset=(0, 0, 0, 0), anchor="b")
    rows = [["Proof", "Seeded defect", "Finding", "Clause"]]
    for r in [r for r in RUNS if not r["proof"].startswith("ctrl")]:
        f = next(f for f in r["findings"] if f"{f['code']}:{f['element']}" in r["expected"])
        rows.append([[P(f"({r['proof']}) {r['label'].replace('LBL-', '')}", sz=10, b=True)],
                     [P(r["seeded_defect"], sz=10)],
                     [P(PLAIN[f["code"]], sz=10, b=True, color=RED)],
                     [P("; ".join(c for _, c in f["clauses"]).replace("; MDR Annex I ", ", "), sz=10)]])
    s.table("Findings", X, 1.85, [0.82, 1.83, 1.18, 1.2], rows, heights=[0.3, 0.62, 0.48, 0.62, 0.62])
    caught, expected, false, nproofs, review = seeded_summary()
    ty = 1.85 + 0.3 + 0.62 * 3 + 0.48 + 0.12
    s.box("Findings summary", X, ty, Wd, 1.2, [
        P(f"{caught}/{expected} seeded defects caught. {false} false defect flags across {nproofs} proofs "
          f"(4 seeded, 6 clean controls). {review} uncertain OCR reads were routed to a human: twice the small "
          "\"SYN\" tag on a placeholder symbol, once an address read just under the 0.80 confidence threshold.",
          sz=10),
        P("Scenario 2 (pack quantity 10 to 5): 3 box labels affected; new UDI-DI flagged for DE and FR under MDR "
          "Annex VI 3.9(f); US routed to RA, with a GUDID task under 21 CFR 830.310(b)(14).", sz=10),
    ], inset=(0, 0, 0, 0))

    ly = max(1.85 + ph, ty + 1.2) + 0.15
    s.box("Limits", 0.4, ly, 12.53, 1.08, [
        P("Limits of this test", sz=11, b=True, color=BLUE, after=2),
        P("Symbol templates are drawn by the same code that renders the labels, so matching is easier than on "
          "real artwork.", sz=10, bullet=True),
        P("No rotation, no real ISO artwork, no print-quality grading. Proofs are blurred, noised and "
          "JPEG-compressed only.", sz=10, bullet=True),
        P("All data are synthetic: fictional device, company and GTINs, placeholder symbols, simulated approvals. "
          "n = 4 seeded defects is a smoke test, not a validation result.", sz=10, bullet=True),
    ], fill=TINT, geom="roundRect", radius=6000, inset=(0.15, 0.06, 0.15, 0.04))
    return append_shapes(xml, s.xml())


def main():
    skill = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUT
    work = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(TEMPLATE) as z:
        z.extractall(work)
    for after in ("slide2.xml", "slide3.xml", "slide4.xml"):
        subprocess.run([sys.executable, str(skill / "scripts" / "add_slide.py"), str(work), "slide2.xml",
                        "--after", after], check=True, capture_output=True)
    slides = work / "ppt" / "slides"
    media = Media(work)
    for name, fn in [("slide1.xml", build_cover), ("slide2.xml", build_main), ("slide3.xml", build_annex_a),
                     ("slide4.xml", build_annex_b), ("slide5.xml", build_annex_c)]:
        p = slides / name
        p.write_text(fn(p.read_text(encoding="utf-8"), media), encoding="utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        ct = work / "[Content_Types].xml"
        z.write(ct, ct.name)
        for f in sorted(work.rglob("*")):
            if f.is_file() and f != ct:
                z.write(f, f.relative_to(work).as_posix())
    shutil.rmtree(work)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
