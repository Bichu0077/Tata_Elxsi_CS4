# Case Study 4: regulatory and market research

Status: research notes v1, 2026-10-19. Facts only; no design ideas, apart from the final comparison asked for in §3.5.

**Markers**
- **[P]** primary source: the regulation text, the agency page, or the standards body.
- **[S]** secondary source: a consultancy, law firm, vendor or blog.
- **[UNVERIFIED]** the claim could not be confirmed against a primary source in this session.
- Quotes are marked with quotation marks; everything else is a paraphrase.

**Access notes**
- **EUR-Lex** blocked automated access. The MDR text below therefore comes from the Official Journal PDF served by the EU Publications Office: [OJ L 117, 5.5.2017](https://op.europa.eu/o/opportal-service/download-handler?identifier=83bdc18f-315d-11e7-9412-01aa75ed71a1&format=pdf&language=en&productionSystem=cellar). That is the **original 2017 text**. The PDF's reference is the consolidated version of 2023-03-20, which was not retrieved.
- **iso.org** (HTTP 403) and **imdrf.org** (timeout) could not be fetched. The ISO and IMDRF facts are therefore secondary.

---

## 1. What each regulation requires

### 1.1 FDA: 21 CFR Part 801 (general labeling)

Source: [FDA, General Device Labeling Requirements](https://www.fda.gov/medical-devices/device-labeling/general-device-labeling-requirements), PDF reference 1 **[P]**. That page lists the following.

- **Name and place of business (801.1):** the manufacturer, packer or distributor, with street address, city, state and ZIP. If the firm named is not the manufacturer, the name must be qualified, e.g. "Manufactured for…" or "Distributed by…".
- **Intended use (801.4)** and **adequate directions for use (801.5).** The directions must cover:
  - purposes and conditions of use
  - quantity per use
  - frequency
  - duration
  - timing
  - route or method
  - preparation
- **False or misleading statements (801.6)**: a device carrying one is misbranded.
- **Prominence (801.15).** Required information can fail on any of these grounds:
  - panel placement
  - type size
  - contrast
  - crowding
  - non-required content taking the space
- **Language:** all labeling must be in English. The exception is products distributed only in Puerto Rico or a US territory with a different predominant language. If any representation on the label is in a foreign language, all required labeling must also appear in that language.
- **Prescription devices (801.109(b))** must bear "Rx only" or "℞ only", or the "Caution: Federal law restricts this device to sale by or on the order of a ___" statement, plus the method of application or use. Source: [21 CFR 801.109](https://www.law.cornell.edu/cfr/text/21/801.109) **[P]**, via the Cornell LII mirror of the CFR.

### 1.2 FDA UDI rule: 21 CFR 801 Subpart B and Part 830

All sections below come from the CFR text on Cornell LII **[P]**.

| Section | Requirement |
|---|---|
| [801.3](https://www.law.cornell.edu/cfr/text/21/801.3) | **UDI** = device identifier + production identifier. **DI**: "a mandatory, fixed portion of a UDI that identifies the specific version or model of a device" and its labeler. **PI**: "a conditional, variable portion", which holds whichever of these appear on the label: lot or batch, serial number, expiration date, manufacture date, or the HCT/P distinct identification code. **AIDC**: any technology that conveys the UDI "in a form that can be entered into an electronic patient record or other computer system via an automated process." |
| [801.18](https://www.law.cornell.edu/cfr/text/21/801.18) | Dates on the label meant for the user must be in **YYYY-MM-DD** form (four-digit year, then two-digit month, then two-digit day, separated by hyphens, e.g. 2014-01-02). Exceptions: combination products bearing an NDC, and electronic products under Subchapter J. |
| [801.20](https://www.law.cornell.edu/cfr/text/21/801.20) | "The label of every medical device shall bear a unique device identifier (UDI)", and so shall every device package. Exceptions are in 801.30, 801.45 and 801.128(f)(2); 801.55 is the route for requesting others. |
| [801.40](https://www.law.cornell.edu/cfr/text/21/801.40) | The UDI must meet 830.20 and appear in **two forms**: (1) "easily readable plain-text" and (2) AIDC technology. If the AIDC is not evident on visual examination, the label must disclose its presence. Source: search summary of the eCFR and LII text **[P]**. |
| [801.45](https://www.law.cornell.edu/cfr/text/21/801.45) | A device "intended to be used more than once and intended to be reprocessed before each use" must also carry a **permanent direct marking**. The marking may be plain text, AIDC, or an alternative technology. Exceptions: the marking would interfere with safety or effectiveness, or is not technologically feasible. The basis for any exception must be documented in the design and development files. |
| [830.20](https://www.law.cornell.edu/cfr/text/21/830.20) | The UDI must be issued under an FDA-operated system or by an FDA-accredited issuing agency. It must conform to ISO/IEC 15459-2, -4 and -6, and use only the invariant character set of ISO/IEC 646. |
| [830.310](https://www.law.cornell.edu/cfr/text/21/830.310) | **GUDID** data, required for each version or model (14 items): (1) the DI; (2) any DI it replaces; (3) the direct-marking DI or a statement that it matches; (4) brand name; (5) version or model; (6) sterile; (7) natural rubber latex; (8) MRI safety status; (9) size; (10) the types of PI on the label; (11) the premarket submission number or exemption; (12) the FDA listing number; (13) the GMDN term or code; (14) the number of devices per package. |

- **FDA guidance on the form and content of the UDI:** [FDA guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/unique-device-identification-system-form-and-content-unique-device-identifier-udi), PDF reference 7 **[P]**. It is final, dated July 2021, docket FDA-2016-D-1853, and clarifies FDA's interpretation of 801.40.
  - **[UNVERIFIED]** The guidance body was not read; the full text is at [fda.gov/media/99084](https://www.fda.gov/media/99084/download). In particular, it is unconfirmed how the HRI date format of the issuing agency relates to the 801.18 YYYY-MM-DD rule.

### 1.3 EU MDR 2017/745: label, IFU and UDI

**Annex I, Chapter III, Section 23** **[P]**, from the OJ text.

- **23.1, general.** Each device must carry the information needed to identify the device and its manufacturer. If the manufacturer has a website, the information must also be kept up to date there.
  - (a) Medium, format, content, legibility and location must suit the device and its intended user. The IFU must be "written in terms readily understood by the intended user".
  - (b) The label information goes on the device itself. Where that is not practicable, it may go on the unit packaging or multi-device packaging.
  - (c) "Labels shall be provided in a human-readable format and may be supplemented by machine-readable information, such as … (`RFID') or bar codes."
  - (d) The IFU is required, except for class I and IIa devices that can be used safely without one.
  - (e) A single IFU copy is allowed for multiple devices if the purchaser agrees.
  - (f) An electronic IFU is allowed only under Regulation (EU) No 207/2012.
  - (g) Residual risks are to be stated as limitations, contra-indications, precautions or warnings.
  - (h) "Where appropriate, the information supplied by the manufacturer shall take the form of internationally recognised symbols. Any symbol or identification colour used shall conform to the harmonised standards or CS." Where no harmonised standard or CS exists, the symbol must be described in the documentation.
- **23.2, information on the label.** "The label shall bear all of the following particulars", items (a) to (s), 19 in all:
  - (a) name or trade name
  - (b) details needed to identify the device and the pack contents, and the intended purpose if not obvious
  - (c) manufacturer name and registered address
  - (d) authorised representative, if the manufacturer is outside the EU
  - (e) whether the device contains a medicinal substance, human tissues or cells, or animal tissues or cells
  - (f) information per Section 10.4.5
  - (g) lot or serial number "preceded by the words LOT NUMBER or SERIAL NUMBER or an equivalent symbol"
  - (h) "the UDI carrier referred to in Article 27(4) and Part C of Annex VII"
  - (i) use-by date, "at least in terms of year and month"
  - (j) date of manufacture, if there is no use-by date
  - (k) special storage or handling conditions
  - (l) sterile state and sterilisation method
  - (m) warnings or precautions; these may be kept minimal, with detail in the IFU
  - (n) single use, which must be "consistent across the Union"
  - (o) reprocessed single-use device, with the number of cycles done and any limit
  - (p) "custom-made device"
  - (q) "an indication that the device is a medical device", or "exclusively for clinical investigation"
  - (r) qualitative and quantitative composition, for substance-based devices
  - (s) serial number for active implantables; serial or lot number for other implantables
  - Note: (h) cites "Annex VII" as printed in the 2017 OJ text. The UDI carrier rules are in Annex VI Part C. Whether a corrigendum or the consolidated text changes this is **[UNVERIFIED]**.
- **23.3, sterile packaging.** Ten particulars, (a) to (j):
  - recognisable as sterile packaging
  - sterile declaration
  - sterilisation method
  - manufacturer name and address
  - device description
  - "exclusively for clinical investigations"
  - "custom-made device"
  - month and year of manufacture
  - use-by date
  - an instruction to check the IFU if the packaging is damaged or opened
- **23.4, IFU.** Items (a) to (ab). Examples:
  - (a) repeats label items (a), (c), (e), (f), (k), (l), (n) and (r)
  - (b) intended purpose, indications, contra-indications, target groups and users
  - (d) link to the SSCP (Article 32)
  - (g) residual risks and side-effects
  - (y) date of issue or latest revision of the IFU
  - (z) serious-incident reporting notice
  - (ab) requirements for software and IT security
- In the PDF text extraction, "23.3." printed beside the 23.2 lead-in. This looks like a layout artefact; the numbering above follows the headings.

**Articles** **[P]**, from the OJ text.

- **Art. 10(11):** the information in Annex I Section 23 must be "in an official Union language(s) determined by the Member State in which the device is made available to the user or patient." Label particulars must be "indelible, easily legible and clearly comprehensible to the intended user or patient."
  - Member-State language choices vary. For example, Finland accepts Finnish, Swedish or English unless internationally recognised symbols are used: [Fimea](https://fimea.fi/en/medical-devices/placing-a-medical-device-on-the-market/labelling-and-instructions-for-use) **[P, national authority]**.
  - The Commission keeps a language-requirements table; Revision 3 is dated August 2025: [Complife](https://www.complifegroup.com/?p=11903) **[S]**.
- **Art. 27(1).** The UDI is made up of the **UDI-DI**, "specific to a manufacturer and a device", which gives access to the Annex VI Part B data, and the **UDI-PI**, which identifies the unit of production and, if applicable, the packaged devices. The UDI goes on the label or the packaging, and economic operators and health institutions must store it.
- **Art. 27(3):** the UDI is assigned to the device and to all higher packaging levels before the device is placed on the market.
- **Art. 27(4):** "UDI carriers shall be placed on the label of the device and on all higher levels of packaging." Shipping containers are excluded.
- **Art. 27(5):** the UDI is used for serious-incident and field-safety-corrective-action reporting.

**Annex VI Part C: UDI carrier rules** **[P]**.

- **HRI** is "a legible interpretation of the data characters encoded in the UDI carrier". The UDI carrier conveys the UDI "by using AIDC and, if applicable, its HRI."
- **4.1:** the carrier ("AIDC and HRI representation") goes on the label or device and on all higher packaging levels.
- **4.2:** under significant space constraints, the carrier may go on the next higher level.
- **4.3:** individually packaged single-use devices of class I and IIa may carry the UDI on a higher packaging level, unless that level won't reach the user (e.g. home care).
- **4.6:** linear bar codes may carry the DI and PI concatenated or in separate bar codes.
- **4.7:** under significant constraints, AIDC alone is enough. Devices used outside healthcare facilities must still show the HRI, even if that leaves no room for the AIDC.
- **4.8:** the HRI follows the issuing entity's rules.
- **4.9:** if RFID is used, a linear or 2D bar code must also be on the label.
- **4.10:** reusable devices carry a permanent UDI that stays readable after each reprocessing.
- **4.11:** the carrier must stay readable during normal use and throughout the device's lifetime.
- **4.14:** the AIDC must be accessible during normal operation or storage.
- **3.9, when a new UDI-DI is required:** "whenever there is a change that could lead to misidentification of the device and/or ambiguity in its traceability". In particular, a change to any of:
  - (a) name or trade name
  - (b) version or model
  - (c) single-use labelling
  - (d) packaged sterile
  - (e) need for sterilisation before use
  - (f) quantity per package
  - (g) critical warnings or contra-indications, e.g. latex or DEHP

**EC UDI page**, PDF reference 6: [European Commission](https://health.ec.europa.eu/medical-devices-topics-interest/unique-device-identifier-udi_en) **[P]**.

- The **Basic UDI-DI** is "the main key in the database". It links certificates, declarations of conformity, technical documentation and the SSCP.
- The designated issuing entities are **GS1, HIBCC, ICCBBA and IFA** (Implementing Decision (EU) 2019/939), renewed to 27 June 2029 by Decision (EU) 2024/2120.
- A Master UDI-DI applies to contact lenses and to spectacle frames and lenses: Delegated Regulations (EU) 2023/2197, 2025/788 and 2025/1920.

**EUDAMED**

- Commission Decision (EU) 2025/2371, published in the OJ on 27 Nov 2025, declared four modules functional: actor registration, UDI/device registration, notified bodies and certificates, and market surveillance.
- Under Regulation (EU) 2024/1860 their use became **mandatory from 28 May 2026**.
- Sources: [Austrian BASG](https://www.basg.gv.at/en/market-surveillance/official-announcements/detail/verpflichtende-nutzung-der-ersten-vier-module-von-eudamed) **[P, national authority]**; [Osborne Clarke](https://www.osborneclarke.com/insights/eu-triggers-mandatory-eudamed-use-diagnostics-and-medtech-may-2026) **[S]**.
- DNV mentions a 28 Nov 2026 deadline for completing registration, but its scope is **[UNVERIFIED]**: [DNV](https://www.dnv.com/article/eudamed-mandatory-use-what-manufacturers-need-to-know/) **[S]**.

**The MD symbol**

- MDR 23.2(q) requires "an indication that the device is a medical device".
- ISO 15223-1:2021 added 25 symbols, many aligned with the MDR: [StarFish Medical](https://starfishmedical.com/?p=15893) **[S]**.
- That the MD symbol is one of those 25, and its clause number, are **[UNVERIFIED]**; the standard text was not accessible.

### 1.4 ISO 15223-1 and ISO 20417

The PDF's references are ISO 15223-1, with no year given (the link points to iso.org/standard/77326), and ISO 20417:2026.

- **ISO 15223-1:2021** (4th edition, July 2021, replaces 2016). It specifies symbols used to express information supplied for a medical device, on the device, on its packaging or in the accompanying information.
  - It added 25 symbols, including importer, distributor and five sterile-barrier or sterilisation symbols: [ANSI blog](https://blog.ansi.org/ansi/iso-15223-1-2021-medical-devices-symbols/) **[S]**; [StarFish](https://starfishmedical.com/?p=15893) **[S]**.
  - **Amendment 1 (2025-03):** "Addition of defined term for authorized representative and modified EC REP symbol to not be country or region specific": [ISO committee listing](https://committee.iso.org/standard/86270.html) **[P]**, from a search snippet.
- **ISO 20417:2026** (2nd edition, 2026-03) replaces ISO 20417:2021 and has been technically revised. It sets general requirements for information supplied by the manufacturer:
  - identification
  - labelling
  - packaging information
  - marking
  - accompanying documents, including the IFU

  It is a shared framework that product standards draw on.
  - Sources: [ISO listing](https://www.iso.org/standard/20417) **[P]**, from a search snippet; [AFNOR](https://www.boutique.afnor.org/en-gb/standard/iso-204172026/medical-devices-information-to-be-supplied-by-the-manufacturer/xs146641/478903) **[S]**.
  - The EN version was approved by CEN on 21 March 2026 and supersedes EN ISO 20417:2021: [normoff.gov.sk](https://normy.normoff.gov.sk/norma/142677/nahlad/) **[S]**.
  - **[UNVERIFIED]** FDA recognition of the 2026 edition (Rec# 5-149) appears only in a blog: [MedDeviceGuide](https://meddeviceguide.com/blog/iso-20417-2026-information-supplied-manufacturer-fda-recognition-guide).
  - Neither standard is law in itself. The binding requirements remain 21 CFR 801 and the MDR; the standards are a means of meeting them, e.g. MDR 23.1(h) requires symbols that conform to harmonised standards.

### 1.5 IMDRF N52

The PDF's reference 5 links the IMDRF page "Principles of Labelling for Medical Devices and IVD Medical Devices".

- **IMDRF/GRRP WG/N52 FINAL:2019** is dated 21 March 2019: [IMDRF PDF](https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-190321-pl-md-ivd.pdf). It covers the label, the IFU and information for the patient.
- It appears to be **superseded by N52 FINAL:2024 (Edition 2), dated 10 April 2024**: [IMDRF Edition 2 PDF](https://www.imdrf.org/sites/default/files/2024-04/IMDRF%20GRRP%20WG%20N52%20%28Edition%202%29.pdf). That rests on a search summary; the PDF itself timed out, so this is **[UNVERIFIED]**.
- **Edition 2 content** **[S]**:
  - It covers general devices and IVDs, and has short sections on software, lay users and patient information such as implant cards.
  - "As best practice, only one machine-readable format should be on the label"; if there are several, the label should make clear which one to scan: [Casus Consulting](https://casusconsulting.com/new-imdrf-guidance-labelling-safety-and-performance-regulatory-review/).
  - Its e-labelling definition is reused by Malaysia's MDA guidance (7th ed., May 2026): [MDA](https://mda.gov.my/index.php/documents/ukk/4147-may-2026-gd-labelling-requirements-for-medical-device-7th-edition) **[P, national authority]**.
- **[UNVERIFIED]** The full list of N52 principles was not read.

### 1.6 21 CFR Part 11: electronic records and signatures

[21 CFR 11.10](https://www.law.cornell.edu/cfr/text/21/11.10) **[P]** lists the controls required for closed systems:

- (a) validation for accuracy, reliability and consistent performance, and the ability to detect invalid or altered records
- (b) accurate, complete copies that can be read and inspected
- (c) protection of records for the whole retention period
- (d) access limited to authorised people
- **(e) audit trails:** "Use of secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions that create, modify, or delete electronic records. Record changes shall not obscure previously recorded information." Audit trails must be kept at least as long as the records they cover, and be available to the agency.
- (f) operational checks that enforce the sequence of steps
- (g) authority checks
- (h) device checks
- (i) trained staff
- (j) written accountability policies for electronic signatures
- (k) control of system documentation, with revision and change control

**[UNVERIFIED]** 11.50 (signature manifestation), 11.70 (linking signatures to records) and Subpart C were not read in this session.

### 1.7 Software used in the quality system

**QMSR**

- From **2 February 2026**, 21 CFR 820 incorporates ISO 13485:2016 by reference, replacing most of the old QS regulation, including 820.70: [FDA QMSR document](https://www.fda.gov/media/153781/download) **[P]**, from a search snippet.
- **ISO 13485:2016 clause 4.1.6** requires documented procedures for validating computer software used in the QMS, before first use and after changes. "The specific approach and activities associated with software validation and revalidation shall be proportionate to the risk associated with the use of the software." Related clauses are 7.5.6 (process validation) and 7.6 (monitoring and measuring equipment software).
  - Sources: [VDE](https://www.vde.com/topics-de/health/beratung/validierung-von-qms-software) **[S]**; [Complizen](https://www.complizen.ai/post/ai-tool-validation-under-the-qmsr-how-to-validate-ai-tools-and-keep-audit-trails) **[S]**.
  - **[UNVERIFIED]** The quoted wording was not checked against the standard text.

**FDA Computer Software Assurance (CSA)**

- Title: *Computer Software Assurance for Production and Quality Management System Software*. Final, **February 2026** (03/02/2026), docket FDA-2022-D-0795. It supersedes the final guidance of 24 Sep 2025: [FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software) **[P]**.
- **Approach:** risk-based assurance for software used in production or in the quality management system, with more rigor where the risk is higher.
- **Scope:** cloud IaaS, PaaS and SaaS are in scope. Device software functions (SaMD and SiMD) are out of scope: [Hogan Lovells](https://www.hoganlovells.com/en/publications/fda-finalizes-computer-software-assurance-guidance-for-production-and-quality-system-software) **[S]**; [NSF](https://www.nsf.org/life-science-regulatory-news/fda-final-guidance-computer-software-assurance-csa) **[S]**.
- It supersedes Section 6 of the 2002 General Principles of Software Validation **[S]**.
- **[UNVERIFIED]** The framework steps and examples of acceptable records were not read from the guidance PDF.

### 1.8 GS1 for UDI: DataMatrix and GS1-128

**Application identifiers**, from the [GS1 AI dataset](https://ref.gs1.org/ai/GS1_Application_Identifiers.jsonld) **[P]**:

| AI | Title | Format | FNC1 separator required |
|---|---|---|---|
| (01) | GTIN | N2+N14 | No |
| (11) | PROD DATE (YYMMDD) | N2+N6 | No |
| (17) | USE BY or EXPIRY (YYMMDD) | N2+N6 | No |
| (10) | BATCH/LOT | N2+X..20 | Yes |
| (21) | SERIAL | N2+X..20 | Yes |

- In a GS1 UDI, the GTIN is the DI, and (17), (10) and (21) form the PI: [GS1 UK](https://www.gs1uk.org/knowledge-hub/which-barcode-should-i-use-for-udi) **[P, GS1 member organisation]**.
- GS1 DataMatrix supports all GS1 AIs in a small symbol. GS1 UK states that plain Code 128 (as opposed to GS1-128) "is not a compliant GS1 barcode" for UDI **[P]**.
- The AI (17) date is encoded as YYMMDD, while 21 CFR 801.18 requires YYYY-MM-DD for dates printed for the user. How the two interact on the HRI is **[UNVERIFIED]**; see §1.2.

**Print quality**

- GS1 General Specifications, Symbol Specification **Table 6** (regulated healthcare, non-retail): GS1 DataMatrix, minimum X-dimension 0.254 mm, 1X quiet zone, **minimum quality 1.5/08/660**. GS1-128 in Table 5 (logistics) is 1.5/10/660. Table 7 (ink-based direct part marking of medical instruments) is 1.5/08/660.
  - Sources: [GS1 GSCN 16-424](https://www.gs1.org/docs/barcodes/GSCN_16-424_DirectPartMarking.pdf) **[P, 2016 change notice]**; [Elsmar forum transcription](https://elsmar.com/elsmarqualityforum/threads/udi-barcode-datamatrix-verification-solutions.68067/page-2) **[S]**.
  - **[UNVERIFIED]** against the current edition of the General Specifications.
- The notation, as commonly read, means: grade 1.5 (C), measuring aperture in thousandths of an inch, light wavelength in nm. **[UNVERIFIED]**: no primary source for the notation was retrieved.
- Grading methods:
  - **ISO/IEC 15415** (2D symbols): current edition 3, 2024. An overall grade takes 5 scans at different rotations: [Euresys](https://documentation.euresys.com/Products/OPEN_EVISION/OPEN_EVISION/en-us/Content/03_Using/4_Text_and_Code_Reading/9_Code_Grading/ISO-IEC_15415_for_Data_Matrix_and_QR_Codes.htm) **[S]**.
  - **ISO/IEC 15416** (linear symbols): 2016 edition, with a 2025 edition listed by [ANSI](https://webstore.ansi.org/standards/iso/isoiec1541515416automatic) **[S]**.

---

## 2. Evidence for the problem: labeling as a cause of recalls

**FDA recall database, through the openFDA API** **[P]**

- Computed in this session from the `root_cause_description` field. Dataset last updated 2026-10-15; posting dates 2002-12-05 to 2026-10-14.
- Queries:
  - [all records](https://api.fda.gov/device/recall.json?count=root_cause_description.exact&limit=100)
  - [posted 2021–2025](https://api.fda.gov/device/recall.json?search=event_date_posted:%5B20210101+TO+20251231%5D&count=root_cause_description.exact&limit=100)
- **Caveat:** openFDA recall records are per product, and one recall event can cover many products. openFDA itself says to "assume all results are unvalidated".

| FDA root cause | All records (n = 59,481) | Posted 2021–2025 (n = 10,299) |
|---|---|---|
| Error in labeling | 897 (1.51%) | 84 (0.82%) |
| Labeling design | 856 (1.44%) | 146 (1.42%) |
| Labeling Change Control | 604 (1.02%) | 135 (1.31%) |
| Labeling mix-ups | 574 (0.97%) | 29 (0.28%) |
| Labeling False and Misleading | 392 (0.66%) | 13 (0.13%) |
| **Five labeling categories** | **3,323 (5.59%)** | **407 (3.95%)** |
| Incorrect or no expiration date | 187 (0.31%) | 28 (0.27%) |
| **Including expiration date** | **3,510 (5.90%)** | **435 (4.22%)** |
| *For scale:* Device Design | 7,676 (12.90%) | — |
| *For scale:* Packaging, the 4 packaging categories | 4,281 (7.20%) | — |

- In 2021–2025, "Labeling Change Control" accounts for 135 of the 407 labeling records (33%).

**Published analyses**

- **FDA authors, AAOS 2025 abstract:** McNamara, Jiang, Gomes, Harner, *FDA Medical Device Recalls: What Orthopedic Surgeons Should Know*: [abstract PDF](https://index.mirasmart.com/AAOS2025/PDFfiles/AAOS2025-001501.PDF).
  - Covers 9,975 Class I and II recall events, 2014-01-01 to 2023-12-31, counted per event, not per product.
  - Labeling was the cause of **12.5%** of orthopedic recalls versus **6.3%** in other specialties. Packaging: 7.5% versus 3.8%. **[P-adjacent: peer-reviewed abstract by FDA staff]**
- **Sedgwick, *State of the Nation 2025 Product Safety and Recall*, US edition**, via the [UL infographic](https://www.ul.com/sites/default/files/2025-04/Medical%20device%20recalls%20-%20Highlights%20from%202024.pdf) **[S]**:
  - 1,059 device recall events in 2024, up 8.6% on 2023.
  - Device failure was the top cause at 11.1% (118 events).
  - "Mislabeling" was among the next four causes.
  - In Q4 2024, "Mislabeling and manufacturing" had 27 events each.
  - **[UNVERIFIED]** The 2024 full-year share for mislabeling isn't given.
- **Stericycle index, Q3 2014:** labeling, packaging and software problems together made up more than 40% of device recalls in that quarter: [FDAnews](https://www.fdanews.com/articles/168961-most-device-recalls-linked-to-labeling-software-issues) **[S]**. It is a single quarter, and the figure combines three causes.
- **Excluded:** a vendor slide claiming "incorrect labeling 25%" ([Honeywell](https://hcenews.honeywell.com/rs/093-RAU-212/images/HON_SS_IG_TW_Recall_Management.pdf?version=0)). The underlying sample isn't stated, so it doesn't meet the named-source bar.

---

## 3. Existing commercial labeling platforms

Almost every claim in this section comes from the vendors themselves **[S, vendor]**. No independent benchmarks were found.

### 3.1 Loftware (Cloud Enterprise / Spectrum for Medical Device; it owns PRISYM ID)

- **Pages:** [medical device](https://loftware.com/industries/medical-device), [UDI](https://www.loftware.com/solutions/regulations/udi), [Cloud Enterprise MD](https://www.loftware.com/products/spectrum/medical-device).
- **Data sources:** pulls label data from "approved content, trusted ERPs, and other applications that generate serial numbers".
- **Compliance and change control:**
  - support for FDA UDI, EU MDR and Part 11
  - role-based access, document versioning, configurable approval workflows and e-records/e-signatures
  - Development/QA/Production environments for testing changes
  - "automate mass label changes and approvals without creating hundreds of label variations"
- **Integrations:** artwork management (Smartflow) and integration with PLM, MES and ERP.
- Loftware acquired PRISYM ID: [MMH](https://www.mmh.com/article/loftware_acquires_prisym_id/Loftware).
- **AI:** none found for medical-device labeling. A 2024 conference keynote was "to focus on AI": [SC247](https://www.supplychain247.com/topic/tag/Loftware/P30).

### 3.2 Loftware Prisym 360

- **Release 1.17 (2023):** [Loftware](https://pl.loftware.com/about-us/news/press-release/2023/loftware-prisym-360-release-1.17-streamlines-label-and-booklet-creation-for-clinical-supplies).
  - A phrase and translation library covering more than 150 languages and regional variants, which flags missing translations.
  - Master label text is used to generate country-specific variants.
  - Change requests routed to reviewers; e-signatures and an audit log.
  - Its current positioning is clinical-trial labeling; Spectrum is the device edition.
- **AI and change-impact analysis:** none found.

### 3.3 Kallik Veraciti

- Cloud labelling and artwork management for pharma, devices and other regulated sectors: [IntuitionLabs listing](https://intuitionlabs.ai/software/regulatory-affairs-compliance/labeling-and-artwork/kallik-veraciti).
- **"Where Used"** lets users "instantly identify and update every affected label when a change occurs". This is the **closest existing feature to change-impact analysis**, and the claim comes from a listing.
- Audit trails, version control, e-signatures and role-based approvals.
- **AI:** a 2022 knowledge-transfer partnership with Aston University set out to build an ML model for label creation: [Med-Tech News](https://www.med-technews.com/news/Medtech-Regulatory-News/aston-university-and-kallik-ktp-aims-to-enhance-labelling-of/). Whether it shipped is **[UNVERIFIED]**. A 2026 item calls Veraciti "AI-enabled" without detail: [International Pharma](https://international-pharma.com/kallik-strengthens-offering-with-globalvision-partnership-to-double-down-on-quality-control/).
- Integrates with GlobalVision Verify: [GlobalVision help](https://help.globalvision.co/verify/verify-x-kallik-veraciti-integration-user-guide).

### 3.4 Esko (WebCenter / WebCenter Go)

- **Product pages:** [life sciences](https://www.esko.com/products/webcenter-go/life-sciences).
  - compares approved regulatory text against artwork; character-level text comparison "across any layout"
  - spell check in 44 languages
  - Part 11 and EU GMP Annex 11 audit trails and e-signatures
  - a GAMP 5-style validation package
- **AI, blog of 3 July 2025:** [Esko](https://www.esko.com/en/blog/smarter-labeling-ai-automation-compliance-in-life-sciences).
  - "automated proofreading plus", which catches "regulatory mismatches, missing symbols, incorrect phrasing, and deviations from your source content"
  - AI places content onto artwork templates using "logic and defined business rules"
  - ingests structured content, Word and Excel
  - Change-impact analysis is **not** claimed.
- Integrated with GlobalVision Verify.
- Seagen and Pfizer reported a 94% cut in proofing time, from 8 h to 20–30 min **[S, vendor case study]**.

### 3.5 GlobalVision (Verify)

- [Labeling QC page](https://www.globalvision.co/solutions/labeling-quality-control).
- **Comparison:** text, artwork, barcode and Braille inspection, plus PDF-to-print inspection.
- **Barcode grading** reports quality to ISO standards; QR codes are checked too.
- **"Intelligent Proofreading" (2015 release):** applies logic to the artwork's elements to cut false positives by more than 50%. Sources describe it as rule-based; no ML component was found.

### What a graph-based, CV-verified approach would add, judged only on what was found

**Already on the market** (vendor claims):
- controlled phrase and translation libraries with variant generation (Prisym 360, Esko)
- data pulled from ERP and PLM (Loftware)
- where-used lookup across labels (Kallik)
- Part 11 audit trails, e-signatures and staged approval (all four)
- text, artwork and barcode comparison of a revised proof against an approved one, plus barcode grading (Esko, GlobalVision)
- AI proofreading against source content and rule-based content placement (Esko, 2025)

**Not found in any source reviewed:**
1. **Links from label elements to requirements.** No vendor material describes tying each label element to the clause that requires it (e.g. MDR 23.2(g), 21 CFR 801.18) as well as to its source data and change order. The PDF's pain point 8 asks for exactly this. Kallik's "Where Used" maps content to labels, not requirements to labels.
2. **Impact driven by regulation changes.** No vendor describes starting from a change in a regulation or standard (e.g. ISO 15223-1 Amd 1 modifying the EC REP symbol) and propagating it to the affected labels and markets. The impact features found start from a change in content.
3. **Checking the printed label against requirements.** The CV and compare tools found check a revised proof or print against an approved artwork. None was found that checks it against the label's required elements, e.g. whether the HRI matches the AIDC payload, or whether every required 23.2 item is present for that market.
4. **Automatic triggers for a new DI.** No vendor states that it flags a change as needing a new UDI-DI under MDR Annex VI 3.9 or creates the matching GUDID or EUDAMED update.

"Not found" means only that it was absent from the sources above, not that no product does it.
- Academic regulatory knowledge graphs exist, but cover premarket rules rather than label content:
  - MedReg-KG, IEEE BigData 2024: [MDSOAR](https://mdsoar.org/handle/11603/37487)
  - an arXiv preprint on a CFR Title 21 RDF graph, which is **[UNVERIFIED]**: [arXiv 2606.28364](https://arxiv.org/pdf/2606.28364)

---

## 4. Requirements in the PDF's references that cs4_extract.md doesn't have

| PDF ref | Adds |
|---|---|
| 1. FDA general labeling | The English-language rule and its "all required labeling in that language too" condition; 801.15 prominence grounds (type size, contrast, crowding); 801.1 qualifiers ("Manufactured for…"); 801.5 contents of directions for use. |
| 2. EU MDR 2017/745 | 19 label particulars (23.2 a–s), 10 sterile-packaging particulars (23.3), IFU items (23.4 a–ab); language set per Member State (Art. 10(11)); UDI carrier on all higher packaging levels (Art. 27(4)); new-UDI-DI triggers (Annex VI 3.9); AIDC/HRI placement rules (Annex VI Part C 4.1–4.15); eIFU only under Reg. 207/2012; symbols must conform to harmonised standards or CS (23.1(h)). |
| 3. ISO 20417:2026 | The 2026 edition replaces 2021 (technically revised). EN version approved by CEN 21 March 2026. |
| 4. ISO 15223-1 | The current version is 2021 + Amd 1:2025, which modifies the EC REP symbol. An existing symbol changes, which is the "correct versions" problem in pain point 3. |
| 5. IMDRF N52 | Edition 2 (2024) appears to supersede the 2019 edition **[UNVERIFIED]**; best practice of a single machine-readable format per label **[S]**. |
| 6. EC UDI | Basic UDI-DI as the database key; four EU issuing entities (GS1, HIBCC, ICCBBA, IFA), designated to 27 June 2029; Master UDI-DI for contact lenses and spectacles. |
| 7. FDA UDI form and content | Plain-text plus AIDC (801.40); disclose AIDC if not evident; final guidance July 2021. Body not read **[UNVERIFIED]**. |

Requirements from outside the 7 references, found while researching:
- 21 CFR 801.18 date format
- 830.310 GUDID fields
- 801.45 direct marking
- 801.109 Rx only
- Part 11 §11.10
- QMSR / ISO 13485 4.1.6
- FDA CSA (Feb 2026)
- EUDAMED mandatory from 28 May 2026
- GS1 AI formats and print grades
