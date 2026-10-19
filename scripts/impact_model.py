"""Effort model for one change touching 30 labels x 20 languages (the PDF's own example).

Every input is an ESTIMATE (cs4_design.md §7.1), not a measurement. Prints a table and writes
CS4/notes/impact_model.json, which the deck builder reads so the slide numbers match.
"""
import json
from pathlib import Path

LABELS, LANGS = 30, 20
BLOCKS = LABELS * LANGS  # A1: every label carries every language


def today(a):
    return {
        "Impact assessment": a["impact_h"],
        "Redline / artwork modification": LABELS * a["redline_h"],
        "Review of language blocks": BLOCKS * a["block_min"] / 60 * a["reviewers"],
        "Final quality check": LABELS * a["qc_h"],
    }


def platform(a):
    return {
        "Impact assessment": a["confirm_h"],
        "Redline / artwork modification": LABELS * a["layout_h"],
        "Review of language blocks": (LABELS * a["packet_min"] / 60 * a["packet_reviewers"]
                                      + a["flag_rate"] * BLOCKS * a["block_min_flag"] / 60),
        "Final quality check": LABELS * a["qc_evidence_h"],
    }


BASE_TODAY = dict(impact_h=16, redline_h=2, block_min=5, reviewers=3, qc_h=1)
PESS_TODAY = dict(impact_h=8, redline_h=1, block_min=3, reviewers=2, qc_h=0.5)
BASE_PLAT = dict(confirm_h=0.5, layout_h=0.25, packet_min=10, packet_reviewers=2, flag_rate=0.10,
                 block_min_flag=5, qc_evidence_h=0.25)
PESS_PLAT = dict(confirm_h=2, layout_h=0.5, packet_min=20, packet_reviewers=2, flag_rate=0.25,
                 block_min_flag=5, qc_evidence_h=0.5)

CASES = {
    "base": (BASE_TODAY, BASE_PLAT),
    "pessimistic platform only": (BASE_TODAY, PESS_PLAT),
    "pessimistic (both sides)": (PESS_TODAY, PESS_PLAT),
}


def run():
    out = {"assumptions": {"labels": LABELS, "languages": LANGS, "blocks": BLOCKS,
                           "today": {"base": BASE_TODAY, "pessimistic": PESS_TODAY},
                           "platform": {"base": BASE_PLAT, "pessimistic": PESS_PLAT}},
           "cases": {}}
    for name, (t, p) in CASES.items():
        ht, hp = today(t), platform(p)
        tt, tp = sum(ht.values()), sum(hp.values())
        out["cases"][name] = {"today_h": tt, "platform_h": tp, "saved_h": tt - tp,
                              "saved_pct": round(100 * (tt - tp) / tt, 1), "today": ht, "platform": hp}
        print(f"{name:28s} today {tt:6.1f} h  platform {tp:5.1f} h  saved {tt - tp:6.1f} h "
              f"({100 * (tt - tp) / tt:.1f}%)")
        for k in ht:
            print(f"    {k:32s} {ht[k]:6.1f} -> {hp[k]:5.1f}")
    path = Path(__file__).resolve().parents[1] / "notes" / "impact_model.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {path}")
    return out


if __name__ == "__main__":
    run()
