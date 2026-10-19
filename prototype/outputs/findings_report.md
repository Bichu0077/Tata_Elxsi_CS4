# CS4 prototype: findings report (SYNTHETIC DATA)

> Everything here is synthetic: a fictional device, fictional company and GTINs, placeholder symbols (not ISO 15223-1 artwork), simulated approvals. Requirement clauses are real and come from the verified primary sources in `CS4/notes/cs4_research.md`.

Graph: 153 nodes, 323 edges (approval: 4, artwork: 6, attribute: 19, change_order: 2, element: 59, language: 3, market: 3, requirement: 26, rule_change: 1, standard: 2, symbol: 9, translation: 19).

## Scenario 1: regulation change (ISO 15223-1 Amd 1, EC REP)

Traversal from the revised symbol node: `RC-SYN-001 -REVISES-> EC REP(2021) <-RENDERED_AS- element -PLACED_ON-> artwork -FOR_MARKET/IN_LANGUAGE->`.

| Label | Market | Language | Level | Element | Requirements |
|---|---|---|---|---|---|
| LBL-DE-unit | DE (EU) | DE | unit | `el:LBL-DE-unit:auth_rep` | MDR Annex I 23.2(d); MDR Annex I 23.1(h) |
| LBL-DE-box | DE (EU) | DE | box | `el:LBL-DE-box:auth_rep` | MDR Annex I 23.2(d); MDR Annex I 23.1(h) |
| LBL-FR-unit | FR (EU) | FR | unit | `el:LBL-FR-unit:auth_rep` | MDR Annex I 23.2(d); MDR Annex I 23.1(h) |
| LBL-FR-box | FR (EU) | FR | box | `el:LBL-FR-box:auth_rep` | MDR Annex I 23.2(d); MDR Annex I 23.1(h) |

Not affected: LBL-US-unit, LBL-US-box (no element rendered with the revised symbol).

**Change order it would create (draft):**

```
CO-SYN-002  status: DRAFT, awaiting human release (AI never approves)
trigger: RC-SYN-001  ISO 15223-1:2021/Amd 1:2025: modified EC REP symbol (title per ISO listing)
impacted:
  - LBL-DE-unit  DE/DE/unit
  - LBL-DE-box  DE/DE/box
  - LBL-FR-unit  FR/FR/unit
  - LBL-FR-box  FR/FR/box
actions:
  - Replace EC REP placeholder (ISO 15223-1:2021) with the Amd 1 edition on each impacted artwork
  - Regenerate redlines from the graph diff
  - Run compliance rules and CV verification on every regenerated proof
  - Risk-based review packet: diff-only review where CV shows change only in the EC REP region
new UDI-DI check: No MDR Annex VI 3.9 trigger: no product attribute changed
approvals:
  - Regulatory Affairs: pending human e-signature (21 CFR 11.10(e) audit trail)
  - Quality Assurance: pending human e-signature (21 CFR 11.10(e) audit trail)
```

## Scenario 2: product change (pack quantity)

`attr:pack_quantity` 10 -> 5. Rules watching the attribute: MDR Annex VI Part C 3.9(f) (new UDI-DI required on change of quantity of devices provided in a package); 21 CFR 830.310(b)(14) (GUDID: total number of individual devices in the device package).

| Label | Market | Level | Impacted elements | UDI flag |
|---|---|---|---|---|
| LBL-US-box | US (US) | box | `el:LBL-US-box:quantity`, `el:LBL-US-box:udi_carrier (pending RA decision)` | **CHECK WITH REGULATORY AFFAIRS: is a new DI required? (US DI triggers not in catalogue)** |
| LBL-DE-box | DE (EU) | box | `el:LBL-DE-box:quantity`, `el:LBL-DE-box:udi_carrier` | **NEW UDI-DI REQUIRED (MDR Annex VI Part C 3.9(f))** |
| LBL-FR-box | FR (EU) | box | `el:LBL-FR-box:quantity`, `el:LBL-FR-box:udi_carrier` | **NEW UDI-DI REQUIRED (MDR Annex VI Part C 3.9(f))** |

Tasks:

- [EU] Obtain a new UDI-DI for the box packaging level from the issuing entity (MDR Annex VI Part C 3.9(f))
- [EU] Update the EUDAMED UDI/device registration (EUDAMED mandatory use from 28 May 2026)
- [US] Check with regulatory affairs whether a new DI is required (open risk R5)
- [US] Update GUDID devices-per-package; if a new DI is assigned, report the previous DI (21 CFR 830.310(b)(14) and (b)(2))

Not affected: LBL-US-unit, LBL-DE-unit, LBL-FR-unit.

## Scenario 3: verification of seeded-defect proofs

The proofs are rendered after CO-SYN-002 (SIMULATED approval), so the graph pins the Amd 1 EC REP placeholder. Each proof is degraded (blur, noise, JPEG q70) to approximate a scan.

### Proof (a): LBL-US-box (US, EN)

Seeded defect: Lot in the human-readable UDI (2410B) differs from the DataMatrix (2410A). Result: **CAUGHT**; no false defect flags.

| Severity | Finding | Element | Requirement clause | Detail |
|---|---|---|---|---|
| review | OCR_LOW_CONFIDENCE | - | - | 1 OCR line(s) below confidence 0.8; routed to human review |
| major | HRI_AIDC_MISMATCH | udi_carrier | 21 CFR 801.40 | HRI (10) = 2410B but DataMatrix (10) = 2410A |

Decoded DataMatrix: `(01)19506000140015(17)281231(10)2410A(21)BX000045`; OCR'd HRI: `{'01': '19506000140015', '17': '281231', '10': '2410B', '21': 'BX000045'}`

### Proof (b): LBL-US-unit (US, EN)

Seeded defect: 'Rx only' missing on the US label. Result: **CAUGHT**; no false defect flags.

| Severity | Finding | Element | Requirement clause | Detail |
|---|---|---|---|---|
| major | REQUIRED_ELEMENT_MISSING | rx_only | 21 CFR 801.109(b) | Required element 'rx_only' not found on the proof |

Decoded DataMatrix: `(01)09506000140018(17)281231(10)2410A(21)SN000123`; OCR'd HRI: `{'01': '09506000140018', '17': '281231', '10': '2410A', '21': 'SN000123'}`

### Proof (c): LBL-DE-unit (DE, DE)

Seeded defect: Old EC REP placeholder (pre-Amd 1) still used. Result: **CAUGHT**; no false defect flags.

| Severity | Finding | Element | Requirement clause | Detail |
|---|---|---|---|---|
| major | SYMBOL_OUTDATED | auth_rep | MDR Annex I 23.1(h); MDR Annex I 23.2(d) | EC REP placeholder for ISO 15223-1:2021 found; graph pins ISO 15223-1:2021+A1:2025 |
| info | UNLINKED_ELEMENT | ce_mark | - | Element has no verified requirement link in the catalogue (e.g. MDR Art. 20 was not verified in research) |

Decoded DataMatrix: `(01)09506000140018(17)281231(10)2410A(21)SN000123`; OCR'd HRI: `{'01': '09506000140018', '17': '281231', '10': '2410A', '21': 'SN000123'}`

### Proof (d): LBL-FR-box (FR, FR)

Seeded defect: MD symbol (and its caption) missing on an EU label. Result: **CAUGHT**; no false defect flags.

| Severity | Finding | Element | Requirement clause | Detail |
|---|---|---|---|---|
| major | REQUIRED_ELEMENT_MISSING | md | MDR Annex I 23.2(q) | Required element 'md' not found on the proof |
| info | UNLINKED_ELEMENT | ce_mark | - | Element has no verified requirement link in the catalogue (e.g. MDR Art. 20 was not verified in research) |

Decoded DataMatrix: `(01)19506000140015(17)281231(10)2410A(21)BX000045`; OCR'd HRI: `{'01': '19506000140015', '17': '281231', '10': '2410A', '21': 'BX000045'}`

## What the checker missed or flagged falsely

| Proof | Expected | Caught | Missed | False defect flags | Routed to review |
|---|---|---|---|---|---|
| a | HRI_AIDC_MISMATCH:udi_carrier | HRI_AIDC_MISMATCH:udi_carrier | - | - | OCR_LOW_CONFIDENCE: ['NLS'] |
| b | REQUIRED_ELEMENT_MISSING:rx_only | REQUIRED_ELEMENT_MISSING:rx_only | - | - | - |
| c | SYMBOL_OUTDATED:auth_rep | SYMBOL_OUTDATED:auth_rep | - | - | - |
| d | REQUIRED_ELEMENT_MISSING:md | REQUIRED_ELEMENT_MISSING:md | - | - | - |
| ctrl-LBL-DE-box | - | - | - | - | OCR_LOW_CONFIDENCE: ['100ExampleWay,pringfield,A'] |
| ctrl-LBL-DE-unit | - | - | - | - | - |
| ctrl-LBL-FR-box | - | - | - | - | - |
| ctrl-LBL-FR-unit | - | - | - | - | - |
| ctrl-LBL-US-box | - | - | - | - | OCR_LOW_CONFIDENCE: ['NLS'] |
| ctrl-LBL-US-unit | - | - | - | - | - |

- Seeded defects caught: **4/4**; missed: **0**.
- False defect flags: **0** on the 4 proofs, **0** on the 6 clean controls.
- Items routed to human review (not defects): **3** across 10 proofs.
- Info: the CE marking element has no verified requirement link (MDR Art. 20 was not verified), so it is reported as a traceability gap on every EU label.

### Limits of this test

- n = 4 seeded defects and 6 clean controls on synthetic labels rendered by the same code that the checker's templates come from. This is a smoke test, not a validation result (design doc §8 needs n >= 300 per defect class).
- Symbol templates are exact renderings of the placeholders; real ISO artwork, print variation, rotation and scale changes beyond +/-5% are not tested.
- Review flags observed in this run are not label defects: 'NLS' is OCR reading the tiny 'SYN' tag under a placeholder symbol, and the manufacturer address line was read just under the 0.80 confidence threshold. Both are routed to a human, as designed; neither counts as a pass or a fail.
- No print-quality grading (needs an ISO/IEC 15415 verifier).
- OCR drops spaces and returns full-width brackets; the checker normalises both (NFKC, space removal). German/French accents are matched after accent folding.

## Screenshots

- `screens/1_graph_impact.png`
- `screens/2_annotated_label.png`
- `screens/3_findings_table.png`
- `screens/4_product_change_udi.png`
