"""CS4 prototype: requirement-linked label graph on SYNTHETIC data.

Usage:  python run.py            (writes everything to outputs/)
"""
import json
import sys
from pathlib import Path

import networkx as nx

from cs4proto import report
from cs4proto.model import build_graph
from cs4proto.scenarios import apply_change_order, scenario1, scenario2, scenario3

OUT = Path(__file__).resolve().parent / "outputs"


def dump(obj, name):
    (OUT / name).write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    (OUT / "screens").mkdir(parents=True, exist_ok=True)
    G = build_graph()

    s1 = scenario1(G)
    print(f"Scenario 1: {len(s1['impacted'])} artworks impacted by the EC REP revision; "
          f"draft {s1['change_order']['id']}")
    dump(s1, "scenario1_impact.json")
    dump(s1["change_order"], "CO-SYN-002.json")

    s2 = scenario2(G)
    print(f"Scenario 2: {len(s2['impacted'])} artworks impacted; rules: "
          f"{[r['clause'] for r in s2['rules_triggered']]}")
    dump(s2, "scenario2_product_change.json")

    G_post = apply_change_order(G)
    runs = scenario3(G_post, OUT / "proofs")
    for r in runs:
        print(f"Proof {r['proof']:>14}: caught={r['caught']} missed={r['missed']} false={r['false_flags']} "
              f"review={len(r['review_flags'])}")
    dump(runs, "scenario3_findings.json")
    nx.write_graphml(nx.DiGraph((u, v, {"rel": d["rel"]}) for u, v, d in G_post.edges(data=True)),
                     OUT / "graph_edges.graphml")
    dump(nx.node_link_data(G_post, edges="links"), "graph.json")

    screens = ["screens/1_graph_impact.png", "screens/2_annotated_label.png", "screens/3_findings_table.png",
               "screens/4_product_change_udi.png"]
    report.screen_graph_impact(s1, G, OUT / screens[0])
    pick = next(r for r in runs if r["proof"] == "a")
    report.annotate_proof(pick, OUT / screens[1])
    for r in runs:
        if not r["proof"].startswith("ctrl"):
            report.annotate_proof(r, OUT / "proofs" / f"annotated_{r['proof']}.png")
    report.screen_findings_table(runs, OUT / screens[2])
    report.screen_udi_flags(s2, OUT / screens[3])
    (OUT / "findings_report.md").write_text(report.markdown(G_post, s1, s2, runs, screens), encoding="utf-8")
    print(f"Wrote {OUT / 'findings_report.md'} and {len(screens)} screenshots")


if __name__ == "__main__":
    main()
