# Case Study 4: verbatim extract

Source: `case_studies/Case Study 4_HLS_End-to-End Medical Device Labeling Automation Management.pdf` (8 pages).
Everything below the headings is quoted exactly from the PDF, including its spelling and punctuation. `p.N` gives the PDF page. Bold matches the PDF's bold. Bullet glyphs are rendered as Markdown list markers.

---

## 1. The 10 pain points (p.5, under "Proposed Solutions should explicitly address:")

1. **Time-Consuming Manual Process-** Experts manually review specifications, regulations, labels, gaps, redlines, revisions and change documentation. This creates high cycle time, repetitive work, expert dependency and scalability challenges.
2. **Frequent Regulatory Updates -** Teams manually monitor new regulations, revised standards, new/revised symbols, UDI requirements and market-specific requirements. The key risk is missing affected labels.
3. **Symbol Management -** Experts manually determine applicable symbols, correct versions, placement, associated text and market applicability. Errors can cause compliance issues, rework and production delays.
4. **Multiple Sources of Truth -** Relevant information may reside in PLM, ERP, requirements documents, regulatory databases, specifications, spreadsheets, artwork files, previous labels and quality systems.
5. **Expertise Dependency** - Labeling requires product, engineering, regulatory, symbols, UDI, quality, artwork and manufacturing knowledge, creating bottlenecks and training challenges.
6. **Manual Redlining -** Experts manually compare current and required labels and create redlines. Computer vision and document intelligence could automate difference detection.
7. **Repetitive Review -** The same checks—product number, manufacturer, symbols, UDI, dates, warnings, language and formatting—are repeatedly performed and are candidates for rules-based automation.
8. **Traceability -** Teams need to answer why each label element exists and trace it to product data, a requirement, source document, approval and change order.
9. **Variant Explosion** - Multiple products, configurations, markets and languages can create thousands of potential label combinations.
10. **Human Error -** Manual copy/paste, outdated symbols, incorrect identifiers, missing information, inconsistent terminology, wrong revisions and wrong market information can introduce risk.

### Related passages that use the words "pain points" or "challenges" (p.4)

**Problem (Expanded – Real-World Context)**

**Current Industry Challenges:**

Imagine a global manufacturer selling: Cardiac stents, Surgical instruments, Diagnostic devices, Orthopaedic implants across various geographies like United States, Europe, Japan, China, Middle East then, a single product change may require updates to:
- 30+ labels
- 20+ languages
- Multiple packaging levels
- Regional regulatory requirements

The Common Pain Points which are leading to human errors.
1. Manual Data Entry
2. Information is copied between:
   - ERP systems
   - PLM systems
   - Labelling software
   - Regulatory databases

**Regulatory Complexity:**
1. Requirements continuously evolve. Examples:
   - UDI updates
   - New symbols
   - MDR changes
   - Country-specific requirements
2. Review process creating delays. Multiple reviewers manually compare:
   - Old versions
   - New versions
   - Regulatory documents
3. Translation Challenges- Translation inconsistencies may introduce:
   - Safety risks
   - Regulatory observations
   - Product recalls
   - Artwork Verification
4. Visual inspection remains heavily dependent on humans
5. Thousands of parts/devices create enormous operational burden

---

## 2. Traditional flow, 18 steps (p.3, "Business Process in Scope:")

> Traditional Approach:
>
> Product / Design Information → Product Understanding → Identify Applicable Markets → Regulatory Requirement Assessment → Gap Assessment → Identify Labeling Gaps → Gap Addressal → Label Content Development → Redline / Artwork Modification → Stakeholder Review → Regulatory / Quality Approval → Label Revision → Change Order Creation → Document / Configuration Control → Final Quality Check → Label Release → Manufacturing → Production Implementation

As a numbered list (same words, same order):

1. Product / Design Information
2. Product Understanding
3. Identify Applicable Markets
4. Regulatory Requirement Assessment
5. Gap Assessment
6. Identify Labeling Gaps
7. Gap Addressal
8. Label Content Development
9. Redline / Artwork Modification
10. Stakeholder Review
11. Regulatory / Quality Approval
12. Label Revision
13. Change Order Creation
14. Document / Configuration Control
15. Final Quality Check
16. Label Release
17. Manufacturing
18. Production Implementation

---

## 3. Stakeholders (p.3, "Stakeholders Involved:")

- Regulatory Affairs for Regulatory compliance management and Change impact assessment
- Product Owner(s)
- Labeling Engineers for Label creation and maintenance
- Quality Assurance for Verification and validation
- Manufacturing for Print readiness and production release
- Supply Chain for Product traceability
- Clinical Teams for Safety and usage information
- IT & Digital Transformation Teams for Platform implementation

---

## 4. Regulations, standards and authorities named

### p.3
> **Regulatory Authorities (Not limited to):** EU MDR, US FDA, Global Submission

### p.8, "References & Study Material"

1. FDA – General Device Labeling Requirements: https://www.fda.gov/medical-devices/device-labeling/general-device-labeling-requirements
2. EU MDR – Regulation (EU) 2017/745: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02017R0745-20230320
3. ISO 20417:2026 – Information supplied by the manufacturer: https://www.iso.org/standard/88714.html
4. ISO 15223-1 – Symbols used with medical devices: https://www.iso.org/standard/77326.html
5. IMDRF N52 – Principles of Labelling: https://www.imdrf.org/documents/principles-labelling-medical-devices-and-ivd-medical-devices
6. European Commission – Unique Device Identifier (UDI): https://health.ec.europa.eu/medical-devices-topics-interest/unique-device-identifier-udi_en
7. FDA – Unique Device Identification System: Form and Content of UDI: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/unique-device-identification-system-form-and-content-unique-device-identifier-udi

### Other mentions in the body text

- p.2: "Unique Device Identification (UDI)"
- p.4: "UDI updates", "MDR changes"
- p.5: "EU MDR/FDA observations", "Warning letters"
- p.7: "FDA updates", "EU MDR updates", "Global regulations"

---

## 5. The 10 example approaches (pp.6–7, "Potential Approaches")

1. **GenAI Label Authoring Assistant -** Capabilities:
   - Generate compliant label text
   - Regulatory language suggestions
   - Auto-update safety statements
2. **AI Compliance Checker -**Uploads:
   - Label PDF
   - Artwork file

   **AI automatically verifies:**
   - Missing information
   - Symbol usage
   - Regulatory compliance
3. **Smart Change Impact Engine-** When a product parameter changes: AI identifies
   - Impacted labels
   - Impacted markets
   - Required actions
4. **Computer Vision-Based Artwork Validation -**System compares:
   - Approved artwork
   - Revised artwork

   Automatically identifies:
   - Text changes
   - Barcode changes
   - Layout deviations
5. **Autonomous Regulatory Intelligence Bot -** Continuously monitors:
   - FDA updates
   - EU MDR updates
   - Global regulations

   Provides proactive alerts.
6. **Smart Translation Validation Platform -** Uses AI to:
   - Validate translations
   - Detect inconsistencies
   - Suggest harmonized terminology
7. **Voice/Prompt to Label Creation-** Users describe product changes verbally/written. AI automatically:
   - Creates draft labels
   - Generates change requests
   - Initiates approval workflows
8. **Predictive Label Quality Analytics -** System predicts below before release:
   - Potential errors
   - High-risk products
   - Compliance failures
9. **Augmented Reality Label Verification -** Using AR glasses/mobile devices:
   - Real-time label inspection
   - Visual discrepancy alerts
   - Guided quality checks
10. **Agentic AI Labeling Ecosystem (Future Vision) -** Multiple AI agents collaborate to:
    - Write labels (Design & Development of labels)
    - Validate compliance
    - Review changes
    - Execute workflows
    - Generate audit records with minimal human intervention.

---

## 6. Evaluation criteria (p.6, "Evaluation Criteria")

- Understanding of labeling problem
- Regulatory/compliance awareness
- Innovation ideas considering Label Design using AI
- AI/automation platform
- End-to-end process coverage
- Accuracy & validation approach
- Traceability & auditability

---

## 7. Stated deliverables and expected outputs

The PDF has no section titled "Deliverables". These are the passages that state what is expected or what is to be produced.

### p.4
> Expectation: New Approach using AI with artifacts or supported data

### p.6, "Recommended Steps"
- Discover & Identify the Manual activities, Process bottlenecks, Error-prone tasks to create Process Map
- Analyse & Perform Root cause analysis/Failure Mode Analysis/Value Stream Mapping to create Automation Opportunity Matrix
- Innovate to Identify technologies applicability such as Artificial Intelligence, Generative AI, Machine Learning, Computer Vision, RPA, Cloud Architecture etc.
- Design & development of labels using AI
- Design & create system architecture, Automation workflow
- Measure and evaluate Time reduction, Error reduction, Compliance improvement, Cost savings

### p.5
> **Proposed Solutions should explicitly address:** (the 10 items in §1)

### p.2, theme and brief
> **Theme:** Intelligent Medical Device Labeling Automation Platform
>
> Design innovative, scalable, and compliant solutions that transform the end-to-end medical device labeling lifecycle by leveraging Artificial Intelligence (AI), Machine Learning (ML), Generative AI, Robotics Process Automation (RPA), Computer Vision, Smart Workflows, and Cloud Technologies.
>
> The challenge encourages participants to rethink traditional labeling operations and create future-ready solutions that accelerate regulatory compliance, reduce human effort, minimize errors, and enhance patient safety.
>
> **Key Takeaways:** Rethink traditional medical device labeling operations and create future-ready solutions that accelerate regulatory compliance, reduce human effort and labeling design & implementation cycle time, minimize errors, and enhance patient safety.

### p.3, "Key Takeaways:"
- **Automation** (What manual activities can be eliminated, how can repetitive tasks be automated etc)
- **AI Driven** (AI reviews labels, GenAI generate compliant content etc)
- **Compliance** (meet all the regulatory requirements be embedded into systems)
- **Innovation** (labeling become "self-validating" and labels predict compliance risks before release)
- **Digital Transformation** (Can Industry 4.0 concepts be applied?)
- **Patient Safety** (How can labeling errors be prevented before reaching the market)
