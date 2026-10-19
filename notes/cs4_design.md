# Case Study 4: design notes

Status: design notes v1, 2026-10-19. Built only from `cs4_extract.md` (cited **E§n**) and `cs4_research.md` (cited **R§n**). No slides yet.

**Source and marking rules**

| Mark | Meaning | Slide-bound? |
|---|---|---|
| E§n | Quoted from the case-study PDF (via cs4_extract.md) | Yes |
| R§n [P] | Primary source in cs4_research.md (regulation text, agency, standards body) | Yes |
| ⚠[S] | Secondary source (consultancy, vendor, blog) | Only with the ⚠[S] mark visible |
| ⚠[UNVERIFIED] | Not confirmed against a primary source | No. Design must not depend on it |
| [EST] | Our assumption or estimate, not a fact | Only labelled "estimate" |
| [DESIGN] | Our design choice | Yes, as a proposal |

---

## 0. Core idea

**Store every label as a requirement-linked knowledge graph, not as an artwork file.** Each label element (the LOT field, the UDI carrier, a sterile-method statement, a warning, a symbol) is a node with five mandatory links [DESIGN]:

| Link | To | Answers |
|---|---|---|
| (a) `REQUIRED_BY` | the regulatory clause, e.g. MDR Annex I 23.2(g), 21 CFR 801.20 | "Why is this here?" |
| (b) `SOURCED_FROM` | the product attribute in PLM/ERP that supplies its value | "Where did this value come from?" |
| (c) `TRANSLATED_AS` | approved translations in the phrase library | "Is every language version approved and consistent?" |
| (d) `PLACED_ON` | the artwork version and region where it appears | "Which artworks change if this changes?" |
| (e) `RELEASED_BY` | the change order and e-signed approval | "Who approved it, when, and under which change?" |

This is the PDF's pain point 8 written as a data model: "Teams need to answer why each label element exists and trace it to product data, a requirement, source document, approval and change order" (E§1).

**Differentiators.** These are the gaps the research did not find in any vendor material reviewed (R§3.5). "Not found" means only that they were absent from those sources.

1. **Requirement-to-element links.** Each element is tied to the clause that requires it. The nearest existing feature, "Where Used" (Kallik ⚠[S]), maps content to labels, not requirements to labels.
2. **Regulation-driven change impact.** A change to a regulation or standard is pushed through to the affected labels and markets. The impact features found all start from a content change.
3. **Checking labels against requirements, not just against earlier artwork.** For example: does the human-readable UDI match the DataMatrix payload, and is every element required for that market present? The CV and compare tools found check a proof against an earlier approved artwork.
4. **Automatic new-UDI-DI flags under MDR Annex VI 3.9.**

The brief says "five gaps" but lists four, and R§3.5 found four. See §9, R1.

---

## 1. Discover & Identify the Manual activities, Process bottlenecks, Error-prone tasks to create Process Map

### 1.1 Traditional flow (E§2, verbatim)

> Product / Design Information → Product Understanding → Identify Applicable Markets → Regulatory Requirement Assessment → Gap Assessment → Identify Labeling Gaps → Gap Addressal → Label Content Development → Redline / Artwork Modification → Stakeholder Review → Regulatory / Quality Approval → Label Revision → Change Order Creation → Document / Configuration Control → Final Quality Check → Label Release → Manufacturing → Production Implementation

### 1.2 Problem framing: where errors come from

**p.4 sources of human error** (E§1, "The Common Pain Points which are leading to human errors" and "Regulatory Complexity"):
- "Manual Data Entry"
- "Information is copied between: ERP systems, PLM systems, Labelling software, Regulatory databases"
- "Requirements continuously evolve" (UDI updates, new symbols, MDR changes, country-specific requirements)
- "Review process creating delays. Multiple reviewers manually compare" (old versions, new versions, regulatory documents)
- "Translation Challenges", "Visual inspection remains heavily dependent on humans"
- "Thousands of parts/devices create enormous operational burden"

**Scale** (E§1): "a single product change may require updates to: 30+ labels, 20+ languages, Multiple packaging levels, Regional regulatory requirements".

**Recall evidence** (R§2 [P]), from openFDA device recall records:

| | All records | Posted 2021–2025 |
|---|---|---|
| Labeling root causes (five categories) | 5.59% of 59,481 | 3.95% of 10,299 |
| Including "Incorrect or no expiration date" | 5.90% | 4.22% |

- In 2021–2025, "Labeling Change Control" accounts for 135 of the 407 labeling records (33%). This is the change process this design targets.
- **Caveats, which must travel with these figures:**
  - Records are per product, and one recall event can cover many products.
  - openFDA says "assume all results are unvalidated".
- An FDA-authored AAOS 2025 abstract counts per recall event (9,975 Class I/II events, 2014–2023). It found labeling caused 12.5% of orthopedic recalls against 6.3% for other specialties (R§2).
- The Sedgwick 2024 figures are ⚠[S] and are kept off slides.

### 1.3 AI-enabled flow

**Step types**
- **A**: automated. Deterministic, logged, no judgement involved.
- **AH**: AI-assisted with a human check. The AI proposes; a named human accepts or rejects.
- **H**: human. A decision or signature that the platform records but does not make.

Module IDs refer to §5.

| # | Traditional step (E§2) | New mode | What happens [DESIGN] | Module |
|---|---|---|---|---|
| 0 | *(new)* Change trigger | A | A product-attribute change in PLM/ERP, an approved regulatory-rule change, or a new market opens a change record. | M0, M2 |
| 1 | Product / Design Information | A | Connectors sync the product attributes into the graph. Each attribute keeps its source-system ID and version. | M0 |
| 2 | Product Understanding | AH | The attributes that drive requirements (sterile, single use, implantable, Rx, pack quantity) are shown with their sources. Attributes extracted from unstructured specs are proposals until the product owner confirms them. | M0 |
| 3 | Identify Applicable Markets | AH | Markets are read from registration and ERP data. RA confirms any market addition. | M0 |
| 4 | Regulatory Requirement Assessment | A / AH | **A**: a graph query returns the requirements that apply to these attributes in these markets. **AH**: new or changed rules come from M2 and enter the graph only after RA approval. | M0, M2 |
| 5 | Gap Assessment | A | Deterministic diff: elements required versus elements present, per label, market and packaging level. | M3 |
| 6 | Identify Labeling Gaps | A | Gap list with clause citations. | M3 |
| 7 | Gap Addressal | AH | M5 proposes content from the approved phrase library. The labeling engineer accepts or edits. | M5 |
| 8 | Label Content Development | AH | The label is assembled from graph elements. No copy and paste. New text is drafted, flagged, and approved by a human before entering the library. | M5 |
| 9 | Redline / Artwork Modification | A / AH | **A**: the redline is generated from the graph diff (old version against new). **AH**: layout changes are proposed and the artwork owner accepts them. | M5, M4 |
| 10 | Stakeholder Review | H | Reviewers get a risk-ranked packet: only the changed elements, each with its clause, source and check results. They no longer compare full documents by hand. | WF |
| 11 | Regulatory / Quality Approval | H | Part 11 e-signature. AI never approves. | WF |
| 12 | Label Revision | A | A new label version is committed to the graph, linked to the approval. | M0 |
| 13 | Change Order Creation | A | The change order is drafted automatically with the complete impacted list from M1. A human releases it through the workflow. | M1, WF |
| 14 | Document / Configuration Control | A | The versioned graph is the configuration record and is synced back to PLM. | M0 |
| 15 | Final Quality Check | AH | M4 verifies the print proof: UDI decode against the human-readable text, required-element presence, symbols, and the proof diff. QA reviews every flag and signs. | M4, WF |
| 16 | Label Release | H | E-signed release. | WF |
| 17 | Manufacturing | A | Released files go to the existing print system. M4 verifies on the line or on a sample, and a failure stops release of that lot's labels. | M4 |
| 18 | Production Implementation | H | Line clearance and first-article sign-off, with M4 evidence attached. | WF |

**Count:** 8 A, 7 AH, 4 H, out of 19 rows (step 0 plus the 18 steps). Steps 4 and 9 are A/AH and are counted as AH. All three approval points (11, 16, 18) and stakeholder review (10) remain human.

---

## 2. Analyse & Perform Root cause analysis/Failure Mode Analysis/Value Stream Mapping to create Automation Opportunity Matrix

All scores are **[EST]**. They are team judgements from the PDF's pain-point descriptions, not measurements, and are to be re-scored with real cycle-time data in a pilot (§7).

**Scale:**
- 1 = low, 3 = high.
- **Effort** = manual effort today.
- **Error risk** = chance and severity of an error escaping.
- **Automation potential** = share that can be made A or AH safely.
- **Priority** = Effort + Error risk + Automation potential (maximum 9).

| # | Step | Effort | Error risk | Automation potential | Priority | Main failure mode (pain point, E§1) | Module |
|---|---|---|---|---|---|---|---|
| 1 | Product / Design Information | 2 | 3 | 3 | 8 | copied or retyped values (PP4, PP10) | M0 |
| 2 | Product Understanding | 2 | 2 | 2 | 6 | expert dependency (PP5) | M0 |
| 3 | Identify Applicable Markets | 1 | 2 | 2 | 5 | wrong market information (PP10) | M0 |
| 4 | Regulatory Requirement Assessment | 3 | 3 | 2 | 8 | missed requirement (PP2, PP5) | M0, M2 |
| 5 | Gap Assessment | 3 | 3 | 3 | **9** | manual review (PP1) | M3 |
| 6 | Identify Labeling Gaps | 2 | 3 | 3 | 8 | missing affected labels (PP2) | M1, M3 |
| 7 | Gap Addressal | 2 | 2 | 2 | 6 | inconsistent terminology (PP10) | M5 |
| 8 | Label Content Development | 3 | 3 | 2 | 8 | copy and paste, outdated symbols (PP3, PP10) | M5 |
| 9 | Redline / Artwork Modification | 3 | 2 | 3 | 8 | manual redlining (PP6) | M5, M4 |
| 10 | Stakeholder Review | 3 | 2 | 2 | 7 | repetitive review (PP7) | WF, M3 |
| 11 | Regulatory / Quality Approval | 2 | 2 | 1 | 5 | human decision by design | WF |
| 12 | Label Revision | 1 | 2 | 3 | 6 | wrong revision (PP10) | M0 |
| 13 | Change Order Creation | 2 | 2 | 3 | 7 | incomplete impacted list (PP2) | M1 |
| 14 | Document / Configuration Control | 2 | 2 | 3 | 7 | wrong revisions (PP10) | M0 |
| 15 | Final Quality Check | 3 | 3 | 3 | **9** | visual inspection depends on humans (E§1) | M4 |
| 16 | Label Release | 1 | 2 | 1 | 4 | human decision by design | WF |
| 17 | Manufacturing | 2 | 3 | 2 | 7 | wrong label printed or used | M4 |
| 18 | Production Implementation | 2 | 2 | 1 | 5 | human decision by design | WF |

**Value-stream view [EST].** The highest-priority steps (5, 15, then 1, 4, 6, 8, 9) are the comparisons and look-ups that the PDF's pain point 7 calls "candidates for rules-based automation". Approvals score lowest because they stay human by design (§6).

---

## 3. Innovate to Identify technologies applicability such as Artificial Intelligence, Generative AI, Machine Learning, Computer Vision, RPA, Cloud Architecture etc.

| Technology (E§7 list) | Where we use it | Where we deliberately don't [DESIGN] |
|---|---|---|
| Knowledge graph (not in the PDF list) | System of record for elements, requirements, sources, translations, artworks and approvals | — |
| Rules engine (deterministic) | Required-element presence, conditional applicability, formats (date, GTIN check digit, GS1 AI syntax), Annex VI 3.9 triggers | — |
| Generative AI / LLM | Retrieval with citations over regulatory sources (M2); free-text checks (M3); drafts of new phrases (M5) | Never decides pass/fail, never approves, never writes into the library without a human |
| Machine learning / CV | Symbol detection, OCR of human-readable text, proof diff (M4) | Barcode print-quality grading stays with an ISO/IEC 15415/15416 verifier (R§1.8) |
| RPA | Connectors to legacy PLM/ERP screens that have no API (M0) | Not used for any decision |
| Cloud architecture | Hosted platform. CSA covers cloud IaaS, PaaS and SaaS ⚠[S] (R§1.7) | — |

---

## 4. Design & development of labels using AI

Labels are **assembled from graph elements**, not drawn freehand [DESIGN]:

1. **Applicable requirements.** For a product × market × packaging level, M0 returns the applicable `Requirement` nodes, e.g. the MDR 23.2 items, filtered by conditions such as "if the device is supplied sterile" for 23.2(l).
2. **Element values.** Each requirement resolves to `Element` nodes whose values come from `SOURCED_FROM` attributes, such as the LOT format, the UDI from the issuing entity, and the use-by date.
3. **Text and symbols.** Text comes from `Phrase` nodes in the approved library, and symbols come from `Symbol` nodes pinned to a standard version.
4. **Layout.** Elements are placed on a market-approved template, one per packaging level. The AI proposes layout changes; humans approve them.
5. **Check.** The result goes through M3 (rules) and M4 (rendered-proof verification) before human review.

**Where GenAI helps, and where it is fenced off**
- It selects candidate phrases and drafts new text. Drafts are always flagged and approved by a human before entering the library.
- It suggests harmonised terminology (E§5, approach 6).
- It drafts the change request from a written description of the change (E§5, approach 7).
- It never produces label text that goes to print without passing through the library and an approval.

**Requirements catalogue, initial seed** (all R§1, [P]):

| ID | Clause | Element / rule |
|---|---|---|
| EU-23.2a | MDR Annex I 23.2(a) | name or trade name |
| EU-23.2c | 23.2(c) | manufacturer name and registered address |
| EU-23.2d | 23.2(d) | authorised representative, if the manufacturer is outside the EU |
| EU-23.2g | 23.2(g) | lot or serial number, "preceded by the words LOT NUMBER or SERIAL NUMBER or an equivalent symbol" |
| EU-23.2h | 23.2(h) | UDI carrier |
| EU-23.2i | 23.2(i) | use-by date, "at least in terms of year and month" |
| EU-23.2l | 23.2(l) | if sterile: sterile state and method |
| EU-23.2n | 23.2(n) | if single use: indication, "consistent across the Union" |
| EU-23.2q | 23.2(q) | indication that the device is a medical device |
| EU-23.3 | 23.3(a)–(j) | sterile-packaging particulars |
| EU-23.1h | 23.1(h) | symbols must conform to harmonised standards or CS |
| EU-A10.11 | Art. 10(11) | language(s) set by each Member State; legibility |
| EU-A27.4 | Art. 27(4) | UDI carrier on the label and all higher packaging levels |
| EU-VI-4.x | Annex VI Part C 4.1–4.15 | AIDC + HRI placement; HRI per issuing entity; HRI mandatory for devices used outside healthcare facilities |
| EU-VI-3.9 | Annex VI Part C 3.9(a)–(g) | new-UDI-DI triggers |
| US-801.1 | 21 CFR 801.1 | name and place of business, with qualifier |
| US-801.15 | 801.15 | prominence |
| US-801.18 | 801.18 | user-facing dates in YYYY-MM-DD |
| US-801.20 | 801.20 | UDI on the label and on every device package |
| US-801.40 | 801.40 | UDI as plain text and as AIDC; disclose the AIDC if not evident |
| US-801.45 | 801.45 | direct marking for reprocessed reusable devices |
| US-801.109 | 801.109(b) | "Rx only" / "℞ only" or the caution statement |
| US-LANG | FDA labeling page | English; if any foreign language is used, all required labeling in that language |
| GS1-AI | GS1 AI dataset | (01) N2+N14; (17) N2+N6 YYMMDD; (10) N2+X..20 with FNC1; (21) N2+X..20 with FNC1 |

Notes on the catalogue:
- **23.2(h).** The 2017 OJ text cites "Annex VII" here, but the carrier rules are in Annex VI Part C ⚠[UNVERIFIED] (R§1.3). We link to Annex VI Part C and record this as open risk R3.
- **The MD symbol.** We implement 23.2(q) as "indication required" without hard-coding which symbol satisfies it. That ISO 15223-1:2021 defines an MD symbol, and its clause number, are ⚠[UNVERIFIED].

---

## 5. Design & create system architecture, Automation workflow

### 5.1 Architecture

```
                 PLM / ERP / RA databases / artwork files / quality systems   (E§1 PP4)
                                         │ connectors (API, RPA where no API)
                                         ▼
 Regulatory sources ──► M2 Regulatory   ┌───────────────────────────────────────────┐
 (FDA, OJ, EC, ISO,     intelligence ──►│ M0  REQUIREMENT-LINKED KNOWLEDGE GRAPH    │
  GS1 change notices)   (proposes; RA   │ Requirement ─REQUIRED_BY─ Element         │
                         approves)      │ Element ─SOURCED_FROM─► ProductAttribute  │
                                        │ Element ─RENDERED_AS─► Phrase / Symbol(v) │
          M6 UDI-DI change detector ◄──►│ Phrase ─TRANSLATED_AS─► Translation(lang) │
          M1 Change-impact engine   ◄──►│ Element ─PLACED_ON─► ArtworkVersion(level)│
          M5 Authoring & translation◄──►│ ArtworkVersion ─RELEASED_BY─► CO/Approval │
          M3 Compliance checker     ◄──►│ (all nodes versioned; nothing deleted)    │
                                        └───────────────┬───────────────────────────┘
                                                        │ proofs / printed labels
                                                        ▼
                                          M4 CV verification ──► evidence nodes
                                                        │
          WF  Workflow + e-signature + Part 11 audit trail (wraps every module)
```

**Graph node types [DESIGN]:**
- `Product`, `ProductAttribute` (value, source system, source ID, version)
- `Market`
- `Requirement` (jurisdiction, clause, text excerpt, condition, effective date, version, approved-by)
- `Element`
- `Phrase`, `Translation`
- `Symbol` (standard, edition or amendment, glyph asset)
- `Template`, `ArtworkVersion` (packaging level)
- `ChangeOrder`, `Approval` (signer, meaning, timestamp)
- `Evidence` (check results)
- `AIOutput` (§6)

Every node and edge carries a valid-from / valid-to time, so the graph can answer "what applied on date X".

### 5.2 Modules

**M0 Knowledge graph and ingestion**
- **Inputs:** PLM/ERP attributes, registration data, existing approved labels (back-loaded), the phrase library, symbol assets.
- **Outputs:** applicability queries; trace paths for "why is this element here"; version history.
- **Failure handling:**
  - Conflicting values for one attribute from two source systems (PP4) block the affected labels and raise a data-owner task. The platform never picks a winner.
  - An element without a `REQUIRED_BY` link is reported as unjustified content.
  - A required element without a source is reported as a gap.
  - Back-loaded legacy labels count as "untraced" until each element is linked. The share traced is a published KPI (§7).

**M1 Change-impact engine**
- **Inputs:** a changed node, which may be an attribute, requirement, symbol version, phrase or template.
- **Process:** a deterministic graph traversal to every dependent `Element` → `ArtworkVersion` → market × packaging level × language.
- **Outputs:** the impacted list, with the path explaining each hit; a change-order draft; tasks for M5, M3, M4 and M6.
- **Failure handling:**
  - The traversal is only as complete as the links.
  - Labels marked "untraced" that might be affected are listed separately as "possibly impacted, manual check". They are never silently left out, since PP2's key risk is "missing affected labels".

**M2 Regulatory intelligence**
- **Inputs:** monitored sources (FDA guidance and CFR, Official Journal, EC UDI pages, ISO amendment notices, GS1 change notices).
- **Access constraint, from R0:** EUR-Lex blocked automated access and iso.org returned 403. Production therefore needs licensed standards access and Publications Office downloads, and may need manual upload of documents.
- **Process:** retrieval over stored source text; an LLM summarises the change and proposes edits to `Requirement` and `Symbol` nodes.
- **Outputs:** a proposed rule change (a diff against the graph) with exact source citations: document, version, clause and quoted passage.
- **Failure handling:**
  - A proposal without a citation, or whose cited passage is not found verbatim in the stored source, is discarded automatically.
  - Ambiguous applicability goes to the RA queue as a question, not a rule.
  - Nothing enters the graph until RA approves and signs.

**M3 Compliance checker**
- **Inputs:** a label version (graph form, plus extracted text from the rendered proof); the applicable requirements.
- **Process:**
  1. **Deterministic rules first**, which carry pass/fail authority. Examples:
     - presence of every applicable requirement
     - conditional rules (sterile → 23.2(l) and 23.3)
     - date format to 801.18 on US user-facing dates
     - GTIN check digit and GS1 AI syntax
     - LOT/SN prefix or symbol per 23.2(g)
     - "Rx only" wording per 801.109(b)
     - language set per market
  2. **LLM only for free text**, e.g. whether a warning on the label is consistent with the IFU, or whether terminology is consistent. LLM findings are **always flagged "AI finding, human review"** and never count as a pass.
- **Outputs:** findings, each with a clause citation, severity and evidence.
- **Failure handling:** a rule that cannot be evaluated (missing data) is a fail, never a skip.

**M4 CV verification**
- **Inputs:** the rendered proof (PDF), print-proof scans, line-sample images; the expected element list from M0.
- **Checks:**
  1. **DataMatrix decode against OCR of the human-readable UDI.** Decode the GS1 element string and parse the AIs ((01) GTIN-14 with check digit, (17), (10), (21)). OCR the HRI and compare field by field, so that 801.40's two forms and Annex VI 4.1's AIDC + HRI are shown to carry the same UDI.
     - Dates are compared **by value**, not by string format, until R4 (the YYMMDD versus YYYY-MM-DD question) is resolved.
  2. **Required-element presence per market:** each expected element must be located on the artwork.
  3. **Symbol detection,** matched against `Symbol` assets for the **pinned edition**, so that an outdated glyph fails (PP3, "outdated symbols" in PP10).
  4. **Proof diff:** text-layer and pixel diff against the last approved artwork. Any change outside the regions M1 predicted is flagged.
- **Outputs:** `Evidence` nodes with images, bounding boxes, decoded values and confidence.
- **Failure handling:**
  - A decode failure is a hard fail.
  - Low OCR or detection confidence means abstain and route to a human; it never auto-passes.
  - M4 does **not** grade print quality. That needs an ISO/IEC 15415/15416 verifier, and the GS1 grade threshold is ⚠[UNVERIFIED] (R§1.8).

**M5 Authoring and translation**
- **Inputs:** gaps from M3; impacted elements from M1; the approved phrase library (per language).
- **Process:** select library phrases. When a phrase is missing, an LLM drafts it, flagged as draft, and a human author and linguist approve it into the library.
- **Translation checks:**
  - every required language for the market is present (Art. 10(11) set per Member State; US-LANG)
  - the same source phrase always maps to the same approved translation
  - flag terminology drift
- Machine translation is only ever a flagged draft.
- **Outputs:** the assembled label version; the redline (graph diff rendered on the artwork).
- **Failure handling:** a missing translation blocks the label for that market and is never replaced by fallback text.

**M6 UDI-DI change detector**
- **Inputs:** attribute diffs from M1.
- **Process:** a rule check against MDR Annex VI 3.9 (a)–(g):
  - (a) name or trade name
  - (b) version or model
  - (c) single-use labelling
  - (d) packaged sterile
  - (e) sterilisation before use
  - (f) quantity per package
  - (g) critical warnings or contra-indications
- **Outputs:**
  - "New UDI-DI required (EU)" with the triggering rule.
  - A task to obtain a new DI from the issuing entity (EU: GS1, HIBCC, ICCBBA, IFA).
  - A EUDAMED UDI/device-registration task (mandatory since 28 May 2026, R§1.3).
  - For the US: a GUDID update task, including the previous DI per 830.310(b)(2).
- **Failure handling:** the triggers for a new **US** DI were not researched (R5). For US-marketed products M6 raises "check whether a new DI is needed (US)" for RA, not a verdict.

**WF Workflow, e-signature, audit trail.** Wraps every module. See §6.

### 5.3 Automation workflow: one change end to end

**Scenario A (main): ISO 15223-1 Amendment 1 (2025-03)**

The amendment's title is "Addition of defined term for authorized representative and modified EC REP symbol to not be country or region specific" (R§1.4 [P], from the ISO listing). We know the title only. The new glyph and the amendment's harmonisation status under the MDR were not verified (R6). The walkthrough shows the mechanism, not the glyph.

1. **Detect (M2).** The ISO notice is retrieved. M2 proposes:
   - a new `Symbol` node, "EC REP, ISO 15223-1:2021+A1:2025", superseding "EC REP, ISO 15223-1:2021"
   - a link to requirement EU-23.2d (authorised representative) and EU-23.1h (symbols conform to harmonised standards)
   - a citation of the amendment title
2. **Approve the rule (H, RA).** RA confirms the applicability and sets the effective date, which depends on harmonisation status. Signed and logged.
3. **Impact (M1).** Traversal: `Symbol(EC REP, 2021)` ← `RENDERED_AS` ← `Element(authorised representative)` → `PLACED_ON` → every artwork version that uses it.
   - Output: labels × packaging levels × markets × languages, each with its path.
   - Products of EU manufacturers carry no authorised representative under 23.2(d), so they drop out of the list automatically.
   - Untraced legacy labels are listed separately.
4. **UDI-DI check (M6).** A symbol change is not one of the 3.9 (a)–(g) triggers, so the result is "no new UDI-DI (EU)", logged with the rule checked.
5. **Author (M5).** The symbol asset is swapped in each artwork. Text is unchanged. A redline is generated for each artwork.
6. **Check (M3).** Rules confirm that the EC REP element is present, uses the pinned new symbol, and is accompanied by the authorised representative's name and address (23.2(d)).
7. **Verify (M4).**
   - The proof diff must show changes **only** inside the EC REP region M1 predicted.
   - The UDI decode must still match the HRI.
   - Required elements must still be present.
   - The detected symbol must be the new edition.
8. **Review (H).** A risk-based packet: one representative artwork per template is reviewed in full; the rest are reviewed as diff-only with M4 evidence [DESIGN].
9. **Approve (H, RA/QA).** Part 11 e-signature.
10. **Change order (A, then H).** The change order is drafted with the full impacted list; a human releases it.
11. **Release, print, verify on the line (H, then A).** M4 verifies samples.
12. **Audit.** The trace path from the ISO amendment to each signed artwork is a single query.

**Scenario B (second): product attribute change, pack quantity 10 → 5**

1. **Trigger (A).** PLM changes the pack-quantity attribute on a sterile, single-use device sold in the EU and US.
2. **M6.** The change hits **3.9(f), quantity of devices provided in a package**, so the result is "New UDI-DI required (EU)". Tasks raised:
   - new DI from the issuing entity
   - EUDAMED update
   - for the US: "check whether a new DI is needed (US)" (R5), plus GUDID items 830.310(b)(14) (devices per package) and (b)(2) (previous DI) if a new DI is assigned
3. **M1.** The pack-quantity element and the UDI carrier (DI change) are impacted on every label at that packaging level and on higher levels that state contents, in all markets and languages. The IFU is impacted if it states the pack contents.
4. **M5.** New element values. The DataMatrix and HRI are regenerated from the new DI. Text comes from the library, with the quantity substituted.
5. **M3 and M4.**
   - Rules check the GTIN check digit and AI syntax.
   - M4 checks that the decoded (01) equals the HRI GTIN equals the new DI in the graph.
   - M4 checks that the stated quantity matches the attribute.
6. **Review, approval, change order, release.** As in Scenario A, steps 8–12.

---

## 6. Guardrails

1. **AI never approves.** Approvals (steps 11, 16, 18) and RA's acceptance of rule changes are human e-signatures. The workflow has no code path in which a model output counts as an approval [DESIGN].
2. **Part 11 audit trail.** "Use of secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions that create, modify, or delete electronic records. Record changes shall not obscure previously recorded information." (21 CFR 11.10(e), R§1.6 [P])
   - The graph is append-only, with nothing deleted; this is our implementation of "shall not obscure".
   - Also: access control (11.10(d)), authority checks (11.10(g)), operational sequencing checks (11.10(f)), and revision control of system documentation (11.10(k)).
   - 11.50 and 11.70, on signature manifestation and linking signatures to records, were not read in this session ⚠[UNVERIFIED] and are open risk R8.
3. **Risk-based review.** Review depth scales with the risk of the change [DESIGN]:
   - UDI, warnings, sterile state and use-by date: full review by two people.
   - Symbol swaps with a clean M4 diff: diff-only review.
   - Every AI finding: always reviewed.
4. **The platform is validated as quality-system software.**
   - ISO 13485:2016 clause 4.1.6 applies through the QMSR, in force from 2 Feb 2026 (R§1.7 [P]).
   - FDA *Computer Software Assurance for Production and Quality Management System Software* (final, Feb 2026, R§1.7 [P]).
   - The wording "proportionate to the risk" in 4.1.6 is ⚠[S]/[UNVERIFIED] against the standard text, and the CSA framework steps were not read ⚠[UNVERIFIED].
   - Our plan [DESIGN]: anything that decides label content or pass/fail (M0 queries, M3 rules, M4 decode and comparison, M6) is treated as high process risk and gets scripted tests. Reporting dashboards get lighter assurance.
5. **Every AI output is logged as an `AIOutput` node** with:
   - model name and version
   - prompt/template version
   - full inputs (or hashes for large files)
   - retrieved passages and their source versions
   - the output, confidence, the human decision and the signer

   Any AI-assisted decision can be replayed from this record.
6. **Abstain, don't guess.** Every AI or CV component has a confidence threshold. Below it, the item goes to a human; it never passes automatically.

---

## 7. Measure and evaluate Time reduction, Error reduction, Compliance improvement, Cost savings

### 7.1 Impact model for "a single product change may require updates to: 30+ labels, 20+ languages" (E§1)

**Every number below is [EST]**: an assumption for the model, to be replaced with timestamps from the WF audit trail in a pilot.

**Assumptions**
- A1: every one of the 30 labels carries all 20 languages, giving **600 language blocks**. This is the PDF's lower bound ("30+", "20+"), treated as a worst case for coverage.
- A2: today, each block is compared manually by k = 3 reviewers ("Multiple reviewers manually compare", E§1).
- A3: the change is a single-element change (like Scenario A).

| Activity | Today [EST] | With platform [EST] |
|---|---|---|
| Impact assessment | 16 h | 0.5 h (RA confirms the M1 list) |
| Redline / artwork modification | 30 labels × 2 h = 60 h | automated; 30 × 0.25 h layout check = 7.5 h |
| Review of language blocks | 600 × 5 min × 3 reviewers = 150 h | the diff-only packet: 30 × 10 min × 2 = 10 h; plus flagged items, 10% of 600 × 5 min = 5 h |
| Final quality check | 30 × 1 h = 30 h | 30 × 0.25 h (QA reviews M4 evidence) = 7.5 h |
| **Total effort** | **256 h** | **30.5 h (≈ 88% less)** |

- **Cycle time.** Elapsed time is driven by approval queues, which we have not measured. We claim effort reduction only, and measure elapsed time in the pilot as the time from change trigger to release, read from the audit trail.
- **Error.** No error rates are claimed.
  - Escaped defects = checks × miss probability. The manual miss rate is unknown; it is to be measured with seeded defects (§8).
  - For deterministic checks, the platform's miss probability is bounded by validation. Zero misses in n seeded cases gives a ~95% upper bound of 3/n (the rule of three); for example, n = 300 gives ≤ 1%.
- **Compliance.** These are measured, not estimated:
  - share of elements with a `REQUIRED_BY` link (target 100%)
  - share of releases with a complete trace (requirement → source → approval)
  - time from a regulation's publication to an RA-approved impact list
  - count of "untraced" legacy labels
- **Cost.** Saving = (H_today − H_platform) × loaded hourly rate × changes per year, minus platform and validation cost. No rate or volume is assumed here. Avoided recall cost is **not** quantified: the recall data supports the problem framing, not a causal saving.

### 7.2 Problem framing figures for slides

These are slide-safe if their caveats go with them:
- openFDA: labeling root causes are 5.6% of records (all years) and 4.0% (2021–2025). The figures are per product, and openFDA says to treat the data as unvalidated.
- 33% of the 2021–2025 labeling records are "Labeling Change Control".
- FDA-authored AAOS 2025 abstract: labeling caused 12.5% of orthopedic recalls against 6.3% for other specialties.

---

## 8. Validation approach for each AI component

Pass thresholds marked [EST] are proposals to agree with QA. They are not facts.

| Component | Test set | Metric | Pass |
|---|---|---|---|
| M0 ingestion | Reconciliation against source systems for a pilot product family | Field-level match rate; conflicts detected | 100% of conflicts surfaced; 0 silent overwrites |
| M1 impact | Historical change orders with their manually confirmed impacted lists; plus seeded graph changes | Recall of impacted labels; precision | **Recall 100%** on the test set (missing an affected label is PP2's key risk); precision reported |
| M2 regulatory intelligence | Replay of real changes found in R§1: ISO 20417:2021→2026, ISO 15223-1 Amd 1, EUDAMED Decision 2025/2371, CSA Feb 2026 reissue, plus non-relevant documents | Detection recall; citation validity (cited passage found verbatim in the stored source); RA acceptance rate | Citation validity 100% (enforced automatically); detection recall [EST ≥ 90%] |
| M3 rules | Positive and negative test labels for every rule in the catalogue | Rule correctness | 100% (conventional software verification) |
| M3 LLM free text | Seeded inconsistencies (warning text versus IFU, terminology drift), plus clean controls | Recall, false-positive rate | Advisory only; recall [EST ≥ 80%] at a false-positive rate the reviewers accept |
| M4 CV | Seeded-defect corpus of rendered labels: HRI/AIDC mismatch, missing required element, outdated symbol edition, unexpected text change, wrong language set; plus print scans | Per-class recall, false-positive rate, abstain rate | Safety-critical classes (UDI mismatch, missing element): **0 misses in n ≥ 300** per class, giving ≤ 1% at ~95% by the rule of three; others [EST] |
| M5 translation consistency | Seeded mismatches in the library | Recall | 100% for exact-phrase mismatches; drift [EST] |
| M5 LLM drafts | Drafts compared with what reviewers finally approved | Human edit rate | Monitored only; drafts never bypass approval |
| M6 | One positive and one negative case per 3.9 (a)–(g), plus combined changes | Correctness | 100% |

Revalidation is triggered by any change of model version, prompt version, rule set or symbol library, per 4.1.6 "after changes" (R§1.7).

---

## 9. Coverage matrix: 10 pain points × modules

● primary, ○ supporting. The pain-point names are the PDF's (E§1).

| Pain point | M0 KG | M1 Impact | M2 RegIntel | M3 Checker | M4 CV | M5 Author | M6 UDI-DI | WF |
|---|---|---|---|---|---|---|---|---|
| 1. Time-Consuming Manual Process | ○ | ● | | ● | ● | ○ | | ○ |
| 2. Frequent Regulatory Updates | ○ | ● | ● | | | | | |
| 3. Symbol Management | ● | ○ | ○ | ● | ● | | | |
| 4. Multiple Sources of Truth | ● | | | | | | | |
| 5. Expertise Dependency | ● | | ○ | ● | | ○ | ○ | |
| 6. Manual Redlining | | ○ | | | ● | ● | | |
| 7. Repetitive Review | | | | ● | ● | | | ○ |
| 8. Traceability | ● | ○ | | | | | | ● |
| 9. Variant Explosion | ● | ● | | | | ● | | |
| 10. Human Error | ○ | | | ● | ● | ● | ○ | |

Every pain point has at least one primary module.

---

## 10. Rubric map: sections × the 7 evaluation criteria (E§6)

| Criterion (E§6) | Where addressed |
|---|---|
| Understanding of labeling problem | §1.2 problem framing, §1.1 process map, §9 coverage matrix |
| Regulatory/compliance awareness | §4 requirements catalogue, §5.2 M6 (Annex VI 3.9), §6 guardrails (Part 11, QMSR, CSA) |
| Innovation ideas considering Label Design using AI | §0 differentiators, §4 graph-assembled labels, §5.3 Scenario A |
| AI/automation platform | §3 technology applicability, §5.1–5.2 architecture and modules |
| End-to-end process coverage | §1.3 (all 18 steps mapped), §2 matrix, §5.3 two end-to-end scenarios |
| Accuracy & validation approach | §8 validation, §6.4 platform validation, §6.6 abstain rule |
| Traceability & auditability | §0 five links, §5.1 versioned graph, §6.2 audit trail, §6.5 AI output log |

---

## 11. Conflicts and open risks

| # | Item | Effect | Action |
|---|---|---|---|
| R0 | EUR-Lex blocked automated access and iso.org returned 403 (R§ access notes) | M2 cannot just crawl its main sources | Licensed standards subscription; Publications Office PDFs; manual upload path |
| R1 | The brief says "five gaps" but lists four, and R§3.5 found four | A slide claiming five would be unsupported | Use four, or name the fifth from evidence |
| R2 | The MDR text used is the 2017 original, not the 2023 consolidated version the PDF links to | Some clause wording may differ | Check §23 and Annex VI against the consolidated text before slides |
| R3 | 23.2(h) cites "Annex VII"; the carrier rules are in Annex VI Part C ⚠[UNVERIFIED] | Wrong citation in the catalogue | Confirm against a corrigendum or the consolidated text |
| R4 | GS1 AI (17) is YYMMDD; 801.18 requires YYYY-MM-DD; how this applies to the HRI is ⚠[UNVERIFIED] | M3/M4 date rules on the HRI | M4 compares by value; RA to confirm against the FDA UDI guidance body |
| R5 | Triggers for a new US DI were not researched | M6 is EU-only as a verdict | Research the FDA guidance; until then raise a "check" task |
| R6 | ISO 15223-1 Amd 1: only the title is known; glyph and harmonisation status unverified | Scenario A shows the mechanism, not the content | Obtain the amendment; record its harmonisation status |
| R7 | GS1 print-quality grade (1.5/08/660) is ⚠[UNVERIFIED] for the current edition | No grade hard-coded | Leave grading to the verifier; confirm against the current General Specifications |
| R8 | Part 11 §§11.50 and 11.70 not read; CSA framework steps not read | Gaps in guardrails and validation plan detail | Read before Round 2 |
| R9 | IMDRF N52 Edition 2 status is ⚠[UNVERIFIED]; "one machine-readable format per label" is ⚠[S] | Not used as a rule | Confirm from the IMDRF PDF |
| R10 | The MD-symbol clause in ISO 15223-1 is ⚠[UNVERIFIED] | 23.2(q) implemented as "indication required" only | Obtain the standard |
| R11 | The vendor gap analysis rests on vendor marketing ⚠[S]; "not found" ≠ "doesn't exist" | Differentiator claims could be challenged | Slides say "not found in public vendor material reviewed" |
| R12 | openFDA records are per product and unvalidated | Recall shares could be over- or under-stated | Always show the caveat; cite the AAOS per-event figure alongside |
| R13 | The graph is only as complete as its links; legacy labels start "untraced" | M1 recall depends on back-loading | "Possibly impacted" list; publish the share traced |
| R14 | The PDF invites GenAI label generation (E§5 approach 1); we restrict GenAI to drafts behind a phrase library | May read as less ambitious | Present it as the safety design (§6); show where GenAI does act |
| R15 | Member-State language rules come from a Commission table cited only via ⚠[S] | M5 language sets need a primary source | RA approves each market's language node, with a national source (e.g. Fimea [P]) |
| R16 | All effort figures in §7 and all scores in §2 are [EST] | Impact claims are illustrative | Label them "estimate" on slides; replace with pilot data |
