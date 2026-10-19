"""Findings report (markdown) and slide screenshots (Pillow). All outputs are labelled SYNTHETIC."""
from PIL import Image, ImageDraw

from .render import font

NAVY, RED, AMBER, GREEN, GREY, LIGHT, INK = "#1F2A44", "#C62828", "#B45309", "#2E7D32", "#9AA0A6", "#EEF1F6", "#202124"
W, H = 1600, 900
FOOT = "SYNTHETIC DATA - fictional device, placeholder symbols, simulated approvals. CS4 prototype."


def canvas(title, subtitle=""):
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.text((40, 28), title, font=font(34, True), fill=NAVY)
    if subtitle:
        d.text((40, 74), subtitle, font=font(20), fill=INK)
    d.rectangle([0, H - 40, W, H], fill=LIGHT)
    d.text((40, H - 31), FOOT, font=font(16, True), fill=RED)
    return im, d


def box(d, xy, text_lines, fill="white", outline=NAVY, width=2, fnt=None, color=INK):
    d.rounded_rectangle(xy, radius=10, fill=fill, outline=outline, width=width)
    x, y = xy[0] + 12, xy[1] + 8
    for i, t in enumerate(text_lines):
        f = fnt or font(16, i == 0)
        d.text((x, y), t, font=f, fill=color)
        y += f.size + 5


def wrap(text, fnt, width, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


def screen_graph_impact(s1, G, path):
    im, d = canvas("Scenario 1: regulation change -> affected labels by graph traversal",
                   "ISO 15223-1 Amd 1 modifies the EC REP symbol. One query from the revised symbol node.")
    rc = (40, 380, 290, 520)
    box(d, rc, ["Rule change RC-SYN-001", "ISO 15223-1:2021/Amd 1:2025", "EC REP modified", "RA approved (SIMULATED)"],
        fill="#FFF4E5", outline=AMBER)
    sym = (372, 380, 600, 520)
    box(d, sym, ["Symbol node", "EC REP (ISO 15223-1:2021)", "status: REVISED", "placeholder, synthetic"],
        fill="#FDECEA", outline=RED)
    d.line([rc[2], 450, sym[0], 450], fill=AMBER, width=4)
    d.text((rc[2] + 6, 426), "REVISES", font=font(13, True), fill=AMBER)

    items = s1["impacted"]
    n = len(items)
    top, gap, bh = 160, 14, 126
    for i, it in enumerate(items):
        y = top + i * (bh + gap)
        el = (650, y, 930, y + bh - 20)
        aw = (990, y, 1250, y + bh - 20)
        mk = (1310, y, 1560, y + bh - 20)
        box(d, el, ["Element: authorised rep.", it["label"], "REQUIRED_BY:", ", ".join(c.replace("MDR Annex I ", "")
                                                                                      for c in it["requirements"])])
        box(d, aw, ["Artwork", it["artwork"].replace("aw:", ""), f"level: {it['packaging_level']}"], fill="#FDECEA",
            outline=RED, width=3)
        box(d, mk, ["Market / language", f"{it['market']} ({it['jurisdiction']})", f"language: {it['language']}"])
        cy = (el[1] + el[3]) // 2
        d.line([sym[2], 450, el[0], cy], fill=RED, width=3)
        d.line([el[2], cy, aw[0], cy], fill=RED, width=3)
        d.line([aw[2], cy, mk[0], cy], fill=NAVY, width=2)
    d.text((610, top - 34), "RENDERED_AS (reverse)", font=font(14, True), fill=RED)
    d.text((940, top - 34), "PLACED_ON", font=font(14, True), fill=RED)
    d.text((1265, top - 34), "FOR_MARKET / IN_LANGUAGE", font=font(14, True), fill=NAVY)
    y = top + n * (bh + gap) + 4
    na = ", ".join(x["label"] for x in s1["not_impacted"])
    d.text((650, y), f"Not affected: {na}", font=font(17, True), fill=GREY)
    d.text((650, y + 26), "(US labels carry no EC REP element: no path from the revised node)", font=font(15), fill=GREY)
    co = s1["change_order"]
    box(d, (40, 600, 590, 760), [f"{co['id']}  (draft change order)", f"{len(co['impacted_artworks'])} artworks impacted",
                                 "new UDI-DI: no Annex VI 3.9 trigger", "RA + QA e-signatures pending",
                                 "AI never approves"], fill=LIGHT)
    im.save(path)


def annotate_proof(run, path, title=None):
    src = Image.open(run["image"]).convert("RGB")
    lw, lh = src.size
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.text((40, 24), title or f"Proof ({run['proof']}): {run['label']} with findings", font=font(30, True), fill=NAVY)
    d.text((40, 64), f"Seeded defect: {run['seeded_defect']}", font=font(18), fill=INK)
    scale = min(1000 / lw, 740 / lh)
    lab = src.resize((int(lw * scale), int(lh * scale)))
    ox, oy = 30, 100
    im.paste(lab, (ox, oy))
    d.rectangle([ox, oy, ox + lab.width, oy + lab.height], outline=GREY, width=1)
    sx = lambda b: (ox + b[0] * scale, oy + b[1] * scale, ox + b[2] * scale, oy + b[3] * scale)
    major = [f for f in run["findings"] if f["severity"] in ("major", "minor")]
    y = 110
    for i, f in enumerate(major, 1):
        b = f["bbox"]
        if b is not None:  # a missing element has nothing to point at; its callout says so
            r = sx(b)
            d.rectangle([r[0] - 4, r[1] - 4, r[2] + 4, r[3] + 4], outline=RED, width=4)
            d.ellipse([r[2] - 6, r[1] - 22, r[2] + 22, r[1] + 6], fill=RED)
            d.text((r[2] + 2, r[1] - 20), str(i), font=font(18, True), fill="white")
        cl = "; ".join(c for _, c in f["clauses"]) or "approved artwork (no clause)"
        if b is None:
            f = {**f, "message": f["message"] + " (searched the whole proof; required per the graph)"}
        lines = [f"{i}. {f['code']}"] + wrap(f["message"], font(16), 490, d) + wrap(f"Clause: {cl}", font(16, True), 490, d)
        hgt = 14 + len(lines) * 22
        d.rounded_rectangle([1050, y, 1570, y + hgt], radius=8, outline=RED, width=2, fill="#FDECEA")
        for j, t in enumerate(lines):
            d.text((1062, y + 8 + j * 22), t, font=font(16, j == 0 or t.startswith("Clause")), fill=INK)
        y += hgt + 12
    if not major:
        d.text((1050, y), "No defect findings", font=font(18, True), fill=GREEN)
    rev = run["review_flags"]
    if rev:
        d.text((1050, y + 6), f"Routed to human review: {len(rev)} item(s)", font=font(16, True), fill=AMBER)
        y += 30
        for f in rev:
            for t in wrap(f["message"], font(14), 520, d):
                d.text((1050, y + 6), t, font=font(14), fill=AMBER)
                y += 20
    d.rectangle([0, H - 40, W, H], fill=LIGHT)
    d.text((40, H - 31), FOOT, font=font(16, True), fill=RED)
    im.save(path)


def screen_findings_table(runs, path):
    im, d = canvas("Scenario 3: checker results on 4 seeded-defect proofs + 6 clean controls",
                   "DataMatrix decode, OCR of human-readable text, required elements per market from the graph, symbol template match")
    cols = [("Proof", 40, 80), ("Label", 120, 150), ("Seeded defect", 270, 390), ("Checker finding", 660, 420),
            ("Requirement clause", 1080, 290), ("Result", 1370, 190)]
    y = 120
    d.rectangle([30, y, 1570, y + 40], fill=NAVY)
    for name, x, _ in cols:
        d.text((x, y + 9), name, font=font(18, True), fill="white")
    y += 48
    for r in [r for r in runs if not r["proof"].startswith("ctrl")]:
        f = next((f for f in r["findings"] if f"{f['code']}:{f['element']}" in r["expected"]), None)
        cells = [r["proof"], r["label"], r["seeded_defect"],
                 f"{f['code']}: {f['message']}" if f else "-",
                 "; ".join(c for _, c in f["clauses"]) if f else "-",
                 "CAUGHT" if r["caught"] else "MISSED"]
        wrapped = [wrap(c, font(16), w - 14, d) for c, (_, _, w) in zip(cells, cols)]
        hgt = max(len(w) for w in wrapped) * 22 + 16
        d.rectangle([30, y - 4, 1570, y + hgt - 4], fill=LIGHT if r["proof"] in "ac" else "white")
        for (name, x, w), lines in zip(cols, wrapped):
            for j, t in enumerate(lines):
                color = (GREEN if t == "CAUGHT" else RED) if name == "Result" else INK
                d.text((x, y + 4 + j * 22), t, font=font(16, name in ("Proof", "Result")), fill=color)
        if r["false_flags"]:
            d.text((1370, y + 30), f"+{len(r['false_flags'])} false flag(s)", font=font(14, True), fill=AMBER)
        y += hgt
    seeded = [r for r in runs if not r["proof"].startswith("ctrl")]
    ctrl = [r for r in runs if r["proof"].startswith("ctrl")]
    y += 20
    caught = sum(len(r["caught"]) for r in seeded)
    lines = [
        f"Seeded defects caught: {caught}/{sum(len(r['expected']) for r in seeded)}",
        f"False defect flags on the 4 proofs: {sum(len(r['false_flags']) for r in seeded)};"
        f" on 6 clean controls: {sum(len(r['false_flags']) for r in ctrl)}",
        f"Routed to human review (low OCR confidence etc.): {sum(len(r['review_flags']) for r in runs)} item(s) across 10 proofs",
        "Info only: CE marking has no verified requirement link in the demo catalogue (traceability gap, not a defect)",
    ]
    for t in lines:
        d.text((40, y), t, font=font(19, True), fill=NAVY)
        y += 32
    d.text((40, y + 8), "Small synthetic test (n = 4 seeded, 6 clean). Not a validation result.", font=font(17), fill=RED)
    im.save(path)


def screen_udi_flags(s2, path):
    im, d = canvas("Scenario 2: product change -> affected labels and new-UDI-DI rule",
                   f"PLM attribute pack_quantity changed {s2['change']['old']} -> {s2['change']['new']} (box level)")
    box(d, (40, 140, 420, 300), ["Changed attribute", "attr:pack_quantity", f"{s2['change']['old']} -> {s2['change']['new']}",
                                 "source: PLM (synthetic)"], fill="#FFF4E5", outline=AMBER)
    y = 130
    for it in s2["impacted"]:
        eu = it["jurisdiction"] == "EU"
        col = RED if eu else AMBER
        fill = "#FDECEA" if eu else "#FFF4E5"
        lines = [f"{it['label']}  ({it['market']}, {it['language']}, {it['packaging_level']})"]
        lines += ["Impacted: " + ", ".join(e.split(":")[-1] for e in it["elements"])]
        lines += wrap(it["udi_flag"], font(16), 980, d)
        hgt = 16 + len(lines) * 22
        d.rounded_rectangle([500, y, 1560, y + hgt], radius=10, outline=col, width=3, fill=fill)
        for j, t in enumerate(lines):
            d.text((514, y + 8 + j * 22), t, font=font(16, j != 1), fill=col if j >= 2 else INK)
        d.line([420, 220, 500, y + hgt // 2], fill=col, width=3)
        y += hgt + 16
    y += 10
    d.text((500, y), "Not affected: " + ", ".join(x["label"] for x in s2["not_impacted"]) + " (unit labels do not state quantity)",
           font=font(16, True), fill=GREY)
    y = 360
    d.text((40, y), "Tasks raised", font=font(20, True), fill=NAVY)
    y += 34
    for t in s2["tasks"]:
        for j, line in enumerate(wrap(f"[{t['jurisdiction']}] {t['task']} ({t['basis']})", font(15), 420, d)):
            d.text((40, y), line, font=font(15, j == 0), fill=INK)
            y += 21
        y += 8
    im.save(path)


def markdown(G, s1, s2, runs, screens):
    L = ["# CS4 prototype: findings report (SYNTHETIC DATA)", "",
         "> Everything here is synthetic: a fictional device, fictional company and GTINs, placeholder symbols "
         "(not ISO 15223-1 artwork), simulated approvals. Requirement clauses are real and come from the verified "
         "primary sources in `CS4/notes/cs4_research.md`.", "",
         f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges "
         f"({', '.join(f'{t}: {c}' for t, c in sorted(_type_counts(G).items()))}).", ""]
    L += ["## Scenario 1: regulation change (ISO 15223-1 Amd 1, EC REP)", "",
          "Traversal from the revised symbol node: `RC-SYN-001 -REVISES-> EC REP(2021) <-RENDERED_AS- element "
          "-PLACED_ON-> artwork -FOR_MARKET/IN_LANGUAGE->`.", "",
          "| Label | Market | Language | Level | Element | Requirements |", "|---|---|---|---|---|---|"]
    for i in s1["impacted"]:
        L.append(f"| {i['label']} | {i['market']} ({i['jurisdiction']}) | {i['language']} | {i['packaging_level']} | "
                 f"`{i['element']}` | {'; '.join(i['requirements'])} |")
    L += ["", "Not affected: " + ", ".join(f"{x['label']}" for x in s1["not_impacted"]) +
          " (no element rendered with the revised symbol).", "", "**Change order it would create (draft):**", "", "```"]
    co = s1["change_order"]
    L += [f"{co['id']}  status: {co['status']}", f"trigger: {co['trigger']}  {co['reason']}", "impacted:"]
    L += [f"  - {a['label']}  {a['market']}/{a['language']}/{a['packaging_level']}" for a in co["impacted_artworks"]]
    L += ["actions:"] + [f"  - {a}" for a in co["actions"]]
    L += [f"new UDI-DI check: {co['new_udi_di_check']}", "approvals:"]
    L += [f"  - {a['role']}: {a['status']}" for a in co["approvals_required"]] + ["```", ""]
    L += ["## Scenario 2: product change (pack quantity)", "",
          f"`attr:pack_quantity` {s2['change']['old']} -> {s2['change']['new']}. Rules watching the attribute: " +
          "; ".join(f"{r['clause']} ({r['text']})" for r in s2["rules_triggered"]) + ".", "",
          "| Label | Market | Level | Impacted elements | UDI flag |", "|---|---|---|---|---|"]
    for i in s2["impacted"]:
        L.append(f"| {i['label']} | {i['market']} ({i['jurisdiction']}) | {i['packaging_level']} | "
                 f"{', '.join(f'`{e}`' for e in i['elements'])} | **{i['udi_flag']}** |")
    L += ["", "Tasks:", ""] + [f"- [{t['jurisdiction']}] {t['task']} ({t['basis']})" for t in s2["tasks"]]
    L += ["", "Not affected: " + ", ".join(x["label"] for x in s2["not_impacted"]) + ".", ""]
    L += ["## Scenario 3: verification of seeded-defect proofs", "",
          "The proofs are rendered after CO-SYN-002 (SIMULATED approval), so the graph pins the Amd 1 EC REP "
          "placeholder. Each proof is degraded (blur, noise, JPEG q70) to approximate a scan.", ""]
    for r in runs:
        if r["proof"].startswith("ctrl"):
            continue
        L += [f"### Proof ({r['proof']}): {r['label']} ({r['market']}, {r['language']})", "",
              f"Seeded defect: {r['seeded_defect']}. Result: **{'CAUGHT' if r['caught'] else 'MISSED'}**"
              + (f"; false flags: {', '.join(r['false_flags'])}" if r["false_flags"] else "; no false defect flags") + ".", "",
              "| Severity | Finding | Element | Requirement clause | Detail |", "|---|---|---|---|---|"]
        for f in r["findings"]:
            L.append(f"| {f['severity']} | {f['code']} | {f['element']} | "
                     f"{'; '.join(c for _, c in f['clauses']) or '-'} | {f['message']} |")
        dm = r["trace"]["datamatrix"]["decoded"]
        L += ["", f"Decoded DataMatrix: `{dm}`; OCR'd HRI: `{r['trace']['hri']}`", ""]
    seeded = [r for r in runs if not r["proof"].startswith("ctrl")]
    ctrl = [r for r in runs if r["proof"].startswith("ctrl")]
    L += ["## What the checker missed or flagged falsely", "",
          "| Proof | Expected | Caught | Missed | False defect flags | Routed to review |", "|---|---|---|---|---|---|"]
    for r in runs:
        L.append(f"| {r['proof']} | {', '.join(r['expected']) or '-'} | {', '.join(r['caught']) or '-'} | "
                 f"{', '.join(r['missed']) or '-'} | {', '.join(r['false_flags']) or '-'} | "
                 f"{'; '.join(f['code'] + ': ' + str(f['evidence'].get('lines', '')) for f in r['review_flags']) or '-'} |")
    L += ["", f"- Seeded defects caught: **{sum(len(r['caught']) for r in seeded)}/{sum(len(r['expected']) for r in seeded)}**; "
              f"missed: **{sum(len(r['missed']) for r in seeded)}**.",
          f"- False defect flags: **{sum(len(r['false_flags']) for r in seeded)}** on the 4 proofs, "
          f"**{sum(len(r['false_flags']) for r in ctrl)}** on the 6 clean controls.",
          f"- Items routed to human review (not defects): **{sum(len(r['review_flags']) for r in runs)}** across 10 proofs.",
          "- Info: the CE marking element has no verified requirement link (MDR Art. 20 was not verified), so it is "
          "reported as a traceability gap on every EU label.",
          "", "### Limits of this test", "",
          "- n = 4 seeded defects and 6 clean controls on synthetic labels rendered by the same code that the checker's "
          "templates come from. This is a smoke test, not a validation result (design doc §8 needs n >= 300 per defect class).",
          "- Symbol templates are exact renderings of the placeholders; real ISO artwork, print variation, rotation and "
          "scale changes beyond +/-5% are not tested.",
          "- Review flags observed in this run are not label defects: 'NLS' is OCR reading the tiny 'SYN' tag under a "
          "placeholder symbol, and the manufacturer address line was read just under the 0.80 confidence threshold. "
          "Both are routed to a human, as designed; neither counts as a pass or a fail.",
          "- No print-quality grading (needs an ISO/IEC 15415 verifier).",
          "- OCR drops spaces and returns full-width brackets; the checker normalises both (NFKC, space removal). "
          "German/French accents are matched after accent folding.", "",
          "## Screenshots", ""] + [f"- `{p}`" for p in screens]
    return "\n".join(L) + "\n"


def _type_counts(G):
    c = {}
    for _, d in G.nodes(data=True):
        c[d["type"]] = c.get(d["type"], 0) + 1
    return c
