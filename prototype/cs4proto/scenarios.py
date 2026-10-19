"""The three demo scenarios, run on the SYNTHETIC graph."""
import copy

from .checker import check_proof
from .model import MARKETS, PRODUCT, artworks, in_rel, out_rel
from .render import degrade, render_label

OLD_EC_REP, NEW_EC_REP = "sym:ec_rep_2021", "sym:ec_rep_a1"


def symbol_map(G, aw):
    return {G.nodes[e]["kind"]: s for e in in_rel(G, aw, "PLACED_ON")
            for s in out_rel(G, e, "RENDERED_AS") if s.startswith("sym:")}


def describe(G, aw):
    a = G.nodes[aw]
    return {"artwork": aw, "label": a["label"], "market": a["market"], "jurisdiction": MARKETS[a["market"]][0],
            "language": a["lang"], "packaging_level": a["level"]}


def new_udi_di_check(G, changed_attrs):
    """M6: which MDR Annex VI 3.9 / GUDID rules watch the changed attributes."""
    hits = []
    for attr in changed_attrs:
        for r in in_rel(G, f"attr:{attr}", "WATCHES"):
            hits.append({"attribute": attr, "requirement": r.split(":", 1)[1], "clause": G.nodes[r]["clause"],
                         "text": G.nodes[r]["text"], "jurisdiction": G.nodes[r]["jurisdiction"]})
    return hits


def scenario1(G):
    """Regulation change: ISO 15223-1 Amd 1 modifies the EC REP symbol. Graph traversal finds the impact."""
    G.add_node("rc:RC-SYN-001", type="rule_change",
               title="ISO 15223-1:2021/Amd 1:2025: modified EC REP symbol (title per ISO listing)",
               status="approved by RA (SIMULATED)", note="new glyph not verified; synthetic placeholder used")
    G.add_edge("rc:RC-SYN-001", OLD_EC_REP, rel="REVISES")
    G.add_edge("rc:RC-SYN-001", NEW_EC_REP, rel="INTRODUCES")
    G.nodes[OLD_EC_REP]["status"] = "revised"

    impacted = []
    for el in in_rel(G, OLD_EC_REP, "RENDERED_AS"):
        for aw in out_rel(G, el, "PLACED_ON"):
            reqs = [r.split(":", 1)[1] for r in out_rel(G, el, "REQUIRED_BY")]
            d = describe(G, aw)
            d.update(element=el, requirements=[G.nodes[f"req:{r}"]["clause"] for r in reqs],
                     path=f"RC-SYN-001 -REVISES-> {OLD_EC_REP} <-RENDERED_AS- {el} -PLACED_ON-> {aw} "
                          f"-FOR_MARKET-> {d['market']} / -IN_LANGUAGE-> {d['language']}")
            impacted.append(d)
    hit = {i["artwork"] for i in impacted}
    not_impacted = [dict(describe(G, aw), reason="no element rendered with the revised symbol")
                    for aw in artworks(G) if aw not in hit]
    udi = new_udi_di_check(G, [])  # a symbol change edits no product attribute
    co = {
        "id": "CO-SYN-002", "status": "DRAFT, awaiting human release (AI never approves)",
        "trigger": "RC-SYN-001", "reason": G.nodes["rc:RC-SYN-001"]["title"],
        "impacted_artworks": [{k: i[k] for k in ("label", "market", "language", "packaging_level")} for i in impacted],
        "actions": ["Replace EC REP placeholder (ISO 15223-1:2021) with the Amd 1 edition on each impacted artwork",
                    "Regenerate redlines from the graph diff",
                    "Run compliance rules and CV verification on every regenerated proof",
                    "Risk-based review packet: diff-only review where CV shows change only in the EC REP region"],
        "new_udi_di_check": "No MDR Annex VI 3.9 trigger: no product attribute changed" if not udi else udi,
        "approvals_required": [{"role": r, "status": "pending human e-signature (21 CFR 11.10(e) audit trail)"}
                               for r in ("Regulatory Affairs", "Quality Assurance")],
        "synthetic": True,
    }
    G.add_node("co:CO-SYN-002", type="change_order", title=co["reason"], status="draft")
    for aw in hit:
        G.add_edge("co:CO-SYN-002", aw, rel="IMPACTS")
    return {"impacted": impacted, "not_impacted": not_impacted, "change_order": co}


def apply_change_order(G):
    """SIMULATED approval of CO-SYN-002: re-pin the EC REP elements to the Amd 1 placeholder."""
    H = copy.deepcopy(G)
    for el in in_rel(H, OLD_EC_REP, "RENDERED_AS"):
        H.remove_edge(el, OLD_EC_REP)
        H.add_edge(el, NEW_EC_REP, rel="RENDERED_AS")
    H.nodes["co:CO-SYN-002"]["status"] = "released (SIMULATED approval)"
    for role in ("RA", "QA"):
        H.add_node(f"appr:CO-SYN-002:{role}", type="approval", role=role, signer=f"{role} reviewer (synthetic)",
                   meaning="approved (SIMULATED)", timestamp="2026-10-19T09:00:00Z")
        H.add_edge("co:CO-SYN-002", f"appr:CO-SYN-002:{role}", rel="APPROVED_BY")
    return H


def scenario2(G, new_qty=5):
    """Product change: pack quantity. Attribute traversal + new-UDI-DI rules."""
    H = copy.deepcopy(G)
    old = H.nodes["attr:pack_quantity"]["value"]
    H.nodes["attr:pack_quantity"]["value"] = str(new_qty)
    rules = new_udi_di_check(H, ["pack_quantity"])
    impacted = []
    for el in in_rel(H, "attr:pack_quantity", "SOURCED_FROM"):
        for aw in out_rel(H, el, "PLACED_ON"):
            d = describe(H, aw)
            jur = d["jurisdiction"]
            dm_el = f"el:{d['label']}:udi_carrier"
            elements = [el]
            if jur == "EU" and any(r["requirement"] == "EU-VI-3.9(f)" for r in rules):
                flag = "NEW UDI-DI REQUIRED (MDR Annex VI Part C 3.9(f))"
                elements.append(dm_el)
            else:
                flag = "CHECK WITH REGULATORY AFFAIRS: is a new DI required? (US DI triggers not in catalogue)"
                elements.append(dm_el + " (pending RA decision)")
            d.update(elements=elements, udi_flag=flag)
            impacted.append(d)
    tasks = [
        {"jurisdiction": "EU", "task": "Obtain a new UDI-DI for the box packaging level from the issuing entity",
         "basis": "MDR Annex VI Part C 3.9(f)"},
        {"jurisdiction": "EU", "task": "Update the EUDAMED UDI/device registration", "basis": "EUDAMED mandatory use from 28 May 2026"},
        {"jurisdiction": "US", "task": "Check with regulatory affairs whether a new DI is required", "basis": "open risk R5"},
        {"jurisdiction": "US", "task": "Update GUDID devices-per-package; if a new DI is assigned, report the previous DI",
         "basis": "21 CFR 830.310(b)(14) and (b)(2)"},
    ]
    return {"change": {"attribute": "pack_quantity", "old": old, "new": str(new_qty)}, "rules_triggered": rules,
            "impacted": impacted, "tasks": tasks,
            "not_impacted": [describe(H, aw) for aw in artworks(H)
                             if aw not in {i["artwork"] for i in impacted}]}


PROOFS = [
    ("a", "LBL-US-box", {"hri": {"10": "2410B"}}, "Lot in the human-readable UDI (2410B) differs from the DataMatrix (2410A)",
     {"HRI_AIDC_MISMATCH:udi_carrier"}),
    ("b", "LBL-US-unit", {"omit": ["rx_only"]}, "'Rx only' missing on the US label", {"REQUIRED_ELEMENT_MISSING:rx_only"}),
    ("c", "LBL-DE-unit", {"symbol_override": {"auth_rep": OLD_EC_REP}}, "Old EC REP placeholder (pre-Amd 1) still used",
     {"SYMBOL_OUTDATED:auth_rep"}),
    ("d", "LBL-FR-box", {"omit": ["md"]}, "MD symbol (and its caption) missing on an EU label", {"REQUIRED_ELEMENT_MISSING:md"}),
]
DEFECT_SEVERITIES = {"major", "minor"}


def key(f):
    return f"{f['code']}:{f['element']}"


def scenario3(G_post, out_dir):
    """Verification on 4 seeded-defect proofs plus 6 clean controls."""
    out_dir.mkdir(parents=True, exist_ok=True)
    runs = []
    cases = [(pid, lbl, dfx, desc, exp) for pid, lbl, dfx, desc, exp in PROOFS]
    cases += [(f"ctrl-{lbl}", lbl, {}, "clean control (no seeded defect)", set())
              for lbl in sorted(G_post.nodes[a]["label"] for a in artworks(G_post))]
    for pid, lbl, dfx, desc, expected in cases:
        aw = f"aw:{lbl}:v1"
        a = G_post.nodes[aw]
        img, _ = render_label(a["market"], a["level"], symbol_map(G_post, aw), PRODUCT, dfx)
        proof = degrade(img, seed=len(runs))
        path = out_dir / f"proof_{pid}.png"
        proof.save(path)
        findings, trace = check_proof(G_post, aw, proof)
        got = {key(f) for f in findings if f["severity"] in DEFECT_SEVERITIES}
        runs.append({"proof": pid, "label": lbl, "market": a["market"], "language": a["lang"], "seeded_defect": desc,
                     "expected": sorted(expected), "findings": findings, "trace": trace, "image": str(path), "caught": sorted(expected & got), "missed": sorted(expected - got),
                     "false_flags": sorted(got - expected),
                     "review_flags": [f for f in findings if f["severity"] == "review"],
                     "info": [f for f in findings if f["severity"] == "info"]})
    return runs
