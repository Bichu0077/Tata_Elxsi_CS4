# CS4 prototype: requirement-linked label graph (SYNTHETIC DATA)

A minimal demo of the design in `../notes/cs4_design.md`. It uses one fictional sterile, single-use device, three markets (US, DE, FR), three languages (EN, DE, FR) and two packaging levels (unit, box).

```
pip install -r requirements.txt
python run.py
```

The script runs end to end in about 30 s on a Windows laptop. The OCR models ship inside the `rapidocr-onnxruntime` wheel, so the first run downloads nothing.

## What it does

| Part | File | Role |
|---|---|---|
| Graph | `cs4proto/model.py` | networkx graph of requirement, element, attribute, translation, symbol, artwork, change-order and approval nodes |
| Labels | `cs4proto/render.py` | Pillow labels with a real GS1 DataMatrix (AIs 01, 17, 10, 21) and a two-line human-readable UDI |
| Checker | `cs4proto/checker.py` | DataMatrix decode, OCR, value comparison, required elements per market, symbol template matching |
| Scenarios | `cs4proto/scenarios.py` | 1: regulation change. 2: product change. 3: verification of seeded-defect proofs |
| Report | `cs4proto/report.py` | `outputs/findings_report.md` plus the slide screenshots in `outputs/screens/` |

Requirement clauses are real. They are limited to those verified against primary sources in `../notes/cs4_research.md`:
- MDR Annex I 23.1(h), 23.2(a)–(q)
- MDR Annex VI Part C 3.9(a)–(g) and 4.1
- 21 CFR 801.1, 801.18, 801.20, 801.40, 801.109(b) and 830.310(b)(14)

Everything else is fictional:
- the product, the company and the GTINs (the GTINs have valid check digits but are not assigned to any product)
- the symbols, which are placeholders and not ISO 15223-1 artwork
- the approvals, which are simulated

## Outputs

- `outputs/findings_report.md`: all three scenarios, every finding with its clause, and the misses and false flags.
- `outputs/screens/1_graph_impact.png`, `2_annotated_label.png`, `3_findings_table.png`, `4_product_change_udi.png`.
- `outputs/proofs/`: the 10 degraded proofs and annotated versions of the 4 defect proofs.
- `outputs/*.json`: scenario results, draft change order `CO-SYN-002`, the graph (node-link JSON) and an edge list in GraphML.
