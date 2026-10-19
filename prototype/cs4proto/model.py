"""Synthetic product, requirement catalogue and the requirement-linked label graph.

Everything here is SYNTHETIC demo data. Requirement clauses are real and were
verified against primary sources in CS4/notes/cs4_research.md (R§1); the
product, company names, GTINs and approvals are fictional.
"""
from datetime import date

import networkx as nx

EU_COUNTRIES = {"DE", "FR"}
MARKETS = {  # market -> (jurisdiction, label language). One language per market is a demo assumption.
    "US": ("US", "EN"),
    "DE": ("EU", "DE"),
    "FR": ("EU", "FR"),
}
LEVELS = ("unit", "box")


def gtin_check_digit(body13: str) -> str:
    """GS1 mod-10 check digit for the first 13 digits of a GTIN-14."""
    total = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(body13)))
    return str((10 - total % 10) % 10)


def make_gtin(body13: str) -> str:
    return body13 + gtin_check_digit(body13)


def gtin_valid(gtin: str) -> bool:
    return len(gtin) == 14 and gtin.isdigit() and gtin_check_digit(gtin[:13]) == gtin[13]


# Fictional device modelled on the PDF p.3 sample label (CE 0123, MD, STERILE EO, Rx Only, UDI).
PRODUCT = {
    "name": "NovaFlow-S Infusion Catheter",
    "model": "NF-S-20",
    "manufacturer": "Nova Synthetic Medical Inc., 100 Example Way, Springfield, USA",
    "manufacturer_country": "US",
    "auth_rep": "SynRep GmbH, Musterstr. 1, 00000 Musterstadt, DE",
    "sterile": True,
    "sterilization": "EO",
    "single_use": True,
    "needs_sterilization_before_use": False,
    "critical_warnings": "none",
    "rx": True,
    "pack_quantity": 10,
    "lot": "2410A",
    "serial_unit": "SN000123",
    "serial_box": "BX000045",
    "expiry": date(2028, 12, 31),
    "gtin_unit": make_gtin("0950600014001"),  # fictional, valid check digit, not assigned to any product
    "gtin_box": make_gtin("1950600014001"),
    "notified_body": "0123",
}

# Approved phrase library (SYNTHETIC translations, not linguist-approved).
PHRASES = {
    "device_name": {"EN": "Infusion catheter, sterile, single use",
                    "DE": "Infusionskatheter, steril, zum Einmalgebrauch",
                    "FR": "Cathéter de perfusion, stérile, à usage unique"},
    "sterile": {"EN": "Sterilized using ethylene oxide",
                "DE": "Sterilisiert mit Ethylenoxid",
                "FR": "Stérilisé à l'oxyde d'éthylène"},
    "single_use": {"EN": "Do not reuse", "DE": "Nicht wiederverwenden", "FR": "Ne pas réutiliser"},
    "md": {"EN": "Medical device", "DE": "Medizinprodukt", "FR": "Dispositif médical"},
    "use_by": {"EN": "Use-by date", "DE": "Verwendbar bis", "FR": "Date limite d'utilisation"},
    "quantity": {"EN": "Contents: {n} units", "DE": "Inhalt: {n} Stück", "FR": "Contenu : {n} unités"},
    "rx_only": {"EN": "Rx only"},
}


class Req:
    def __init__(self, rid, jur, clause, text, kind=None, levels=LEVELS, cond=None, watches=None, verified=True):
        self.rid, self.jur, self.clause, self.text = rid, jur, clause, text
        self.kind, self.levels, self.cond, self.watches, self.verified = kind, levels, cond, watches, verified

    def applies(self, product, level):
        return level in self.levels and (self.cond is None or self.cond(product))


outside_eu = lambda p: p["manufacturer_country"] not in EU_COUNTRIES and p["manufacturer_country"] != "EU"

# Short excerpts quoted or paraphrased from the primary text (R§1.2, R§1.3).
REQUIREMENTS = [
    Req("EU-23.2(a)", "EU", "MDR Annex I 23.2(a)", "the name or trade name of the device", "device_name"),
    Req("EU-23.2(b)", "EU", "MDR Annex I 23.2(b)", "details necessary to identify the device and the contents of the packaging", "quantity", levels=("box",)),
    Req("EU-23.2(c)", "EU", "MDR Annex I 23.2(c)", "name of the manufacturer and address of its registered place of business", "manufacturer"),
    Req("EU-23.2(d)", "EU", "MDR Annex I 23.2(d)", "authorised representative, if the manufacturer is outside the Union", "auth_rep", cond=outside_eu),
    Req("EU-23.2(g)", "EU", "MDR Annex I 23.2(g)", "lot or serial number preceded by LOT NUMBER / SERIAL NUMBER or an equivalent symbol", "lot"),
    Req("EU-23.2(h)", "EU", "MDR Annex I 23.2(h)", "the UDI carrier", "udi_carrier"),
    Req("EU-23.2(i)", "EU", "MDR Annex I 23.2(i)", "time limit for using the device, at least year and month", "use_by"),
    Req("EU-23.2(l)", "EU", "MDR Annex I 23.2(l)", "if supplied sterile: its sterile state and the sterilisation method", "sterile", cond=lambda p: p["sterile"]),
    Req("EU-23.2(n)", "EU", "MDR Annex I 23.2(n)", "if intended for single use, an indication of that fact", "single_use", cond=lambda p: p["single_use"]),
    Req("EU-23.2(q)", "EU", "MDR Annex I 23.2(q)", "an indication that the device is a medical device", "md"),
    Req("EU-23.1(h)", "EU", "MDR Annex I 23.1(h)", "any symbol used shall conform to the harmonised standards or CS"),
    Req("EU-VI-C4.1", "EU", "MDR Annex VI Part C 4.1", "UDI carrier (AIDC and HRI representation) on the label and all higher packaging levels", "udi_carrier"),
    Req("EU-VI-3.9(a)", "EU", "MDR Annex VI Part C 3.9(a)", "new UDI-DI required on change of name or trade name", watches="name"),
    Req("EU-VI-3.9(b)", "EU", "MDR Annex VI Part C 3.9(b)", "new UDI-DI required on change of device version or model", watches="model"),
    Req("EU-VI-3.9(c)", "EU", "MDR Annex VI Part C 3.9(c)", "new UDI-DI required on change of 'labelled as single use'", watches="single_use"),
    Req("EU-VI-3.9(d)", "EU", "MDR Annex VI Part C 3.9(d)", "new UDI-DI required on change of 'packaged sterile'", watches="sterile"),
    Req("EU-VI-3.9(e)", "EU", "MDR Annex VI Part C 3.9(e)", "new UDI-DI required on change of 'need for sterilization before use'", watches="needs_sterilization_before_use"),
    Req("EU-VI-3.9(f)", "EU", "MDR Annex VI Part C 3.9(f)", "new UDI-DI required on change of quantity of devices provided in a package", watches="pack_quantity"),
    Req("EU-VI-3.9(g)", "EU", "MDR Annex VI Part C 3.9(g)", "new UDI-DI required on change of critical warnings or contra-indications", watches="critical_warnings"),
    Req("US-801.1", "US", "21 CFR 801.1", "name and place of business of the manufacturer, packer or distributor", "manufacturer"),
    Req("US-801.18", "US", "21 CFR 801.18", "dates for the user in the format YYYY-MM-DD", "use_by"),
    Req("US-801.20", "US", "21 CFR 801.20", "the label of every device, and every device package, shall bear a UDI", "udi_carrier"),
    Req("US-801.40", "US", "21 CFR 801.40", "UDI in easily readable plain text and in AIDC form", "udi_carrier"),
    Req("US-801.109(b)", "US", "21 CFR 801.109(b)", "prescription device label bears 'Rx only' (or the caution statement)", "rx_only", cond=lambda p: p["rx"]),
    Req("US-830.310(b)(14)", "US", "21 CFR 830.310(b)(14)", "GUDID: total number of individual devices in the device package", watches="pack_quantity"),
]
# Content the company puts on labels where no verified clause is in this demo catalogue.
SPEC = Req("SPEC-SYN-001", "ANY", "Company labeling spec (synthetic)", "house content standard", None)
REQ_BY_ID = {r.rid: r for r in REQUIREMENTS}

# Symbols: synthetic placeholders, each pinned to the standard edition it represents.
SYMBOLS = {
    "sym:manufacturer": ("manufacturer", "ISO 15223-1:2021"),
    "sym:ec_rep_2021": ("EC REP", "ISO 15223-1:2021"),
    "sym:ec_rep_a1": ("EC REP (Amd 1)", "ISO 15223-1:2021+A1:2025"),
    "sym:lot": ("LOT", "ISO 15223-1:2021"),
    "sym:use_by": ("use-by date", "ISO 15223-1:2021"),
    "sym:sterile_eo": ("STERILE EO", "ISO 15223-1:2021"),
    "sym:do_not_reuse": ("do not reuse", "ISO 15223-1:2021"),
    "sym:md": ("MD", "ISO 15223-1:2021"),
    "sym:ce": ("CE marking", "n/a (no verified clause in catalogue)"),
}
SYMBOL_FOR_KIND = {"manufacturer": "sym:manufacturer", "auth_rep": "sym:ec_rep_2021", "lot": "sym:lot",
                   "use_by": "sym:use_by", "sterile": "sym:sterile_eo", "single_use": "sym:do_not_reuse",
                   "md": "sym:md", "ce_mark": "sym:ce"}
# Product attribute each element kind takes its value from.
SOURCE_FOR_KIND = {"device_name": ["name"], "manufacturer": ["manufacturer"], "auth_rep": ["auth_rep"],
                   "lot": ["lot"], "use_by": ["expiry"], "sterile": ["sterile", "sterilization"],
                   "single_use": ["single_use"], "md": [], "rx_only": ["rx"], "quantity": ["pack_quantity"],
                   "ce_mark": ["notified_body"]}


def label_kinds(market, level):
    """Element kinds placed on a label (what the artwork carries, not what is required)."""
    jur = MARKETS[market][0]
    kinds = ["device_name", "manufacturer", "lot", "udi_carrier", "use_by", "sterile", "single_use"]
    if jur == "EU":
        kinds += ["auth_rep", "md", "ce_mark"]
    if jur == "US":
        kinds += ["rx_only"]
    if level == "box":
        kinds += ["quantity"]
    return kinds


def required_reqs(product, market, level):
    """Requirements that apply to this label, derived from the catalogue (not from the artwork)."""
    jur = MARKETS[market][0]
    return [r for r in REQUIREMENTS if r.jur == jur and r.kind and r.applies(product, level)]


def udi_fields(product, level):
    return {"01": product[f"gtin_{level}"], "17": product["expiry"].strftime("%y%m%d"),
            "10": product["lot"], "21": product[f"serial_{level}"]}


def build_graph(product=PRODUCT):
    G = nx.DiGraph()
    add = G.add_node
    for r in REQUIREMENTS + [SPEC]:
        add(f"req:{r.rid}", type="requirement", clause=r.clause, text=r.text, jurisdiction=r.jur, verified=r.verified)
    add("std:ISO 15223-1:2021", type="standard", status="current")
    add("std:ISO 15223-1:2021+A1:2025", type="standard", status="not yet adopted")
    G.add_edge("req:EU-23.1(h)", "std:ISO 15223-1:2021", rel="REFERENCES")
    for sid, (name, edition) in SYMBOLS.items():
        add(sid, type="symbol", name=name, edition=edition, synthetic=True)
        if edition.startswith("ISO"):
            G.add_edge(sid, f"std:{edition}", rel="DEFINED_IN")
    for k, v in product.items():
        add(f"attr:{k}", type="attribute", value=str(v), source="PLM (synthetic)")
    for r in REQUIREMENTS:
        if r.watches:
            G.add_edge(f"req:{r.rid}", f"attr:{r.watches}", rel="WATCHES")
    for kind, langs in PHRASES.items():
        for lang, text in langs.items():
            add(f"tr:{kind}:{lang}", type="translation", lang=lang, text=text, status="approved (synthetic)")

    add("co:CO-SYN-001", type="change_order", title="Initial label release", status="released")
    for role in ("RA", "QA"):
        add(f"appr:CO-SYN-001:{role}", type="approval", role=role, signer=f"{role} reviewer (synthetic)",
            meaning="approved", timestamp="2026-01-15T10:00:00Z")
        G.add_edge("co:CO-SYN-001", f"appr:CO-SYN-001:{role}", rel="APPROVED_BY")

    for market, (jur, lang) in MARKETS.items():
        add(f"mkt:{market}", type="market", jurisdiction=jur)
        add(f"lang:{lang}", type="language")
        for level in LEVELS:
            label = f"LBL-{market}-{level}"
            aw = f"aw:{label}:v1"
            add(aw, type="artwork", label=label, market=market, lang=lang, level=level, version=1)
            G.add_edge(aw, f"mkt:{market}", rel="FOR_MARKET")
            G.add_edge(aw, f"lang:{lang}", rel="IN_LANGUAGE")
            G.add_edge(aw, "co:CO-SYN-001", rel="RELEASED_BY")
            reqs = required_reqs(product, market, level)
            for kind in label_kinds(market, level):
                el = f"el:{label}:{kind}"
                add(el, type="element", kind=kind, label=label)
                G.add_edge(el, aw, rel="PLACED_ON")
                linked = [r for r in reqs if r.kind == kind]
                for r in linked:
                    G.add_edge(el, f"req:{r.rid}", rel="REQUIRED_BY")
                if not linked and kind != "ce_mark":
                    G.add_edge(el, f"req:{SPEC.rid}", rel="REQUIRED_BY")
                if kind == "auth_rep":
                    G.add_edge(el, "req:EU-23.1(h)", rel="REQUIRED_BY")
                for a in SOURCE_FOR_KIND.get(kind, []):
                    G.add_edge(el, f"attr:{a}", rel="SOURCED_FROM")
                if kind == "udi_carrier":
                    for a in (f"gtin_{level}", "expiry", "lot", f"serial_{level}"):
                        G.add_edge(el, f"attr:{a}", rel="SOURCED_FROM")
                if kind in SYMBOL_FOR_KIND:
                    G.add_edge(el, SYMBOL_FOR_KIND[kind], rel="RENDERED_AS")
                if kind in PHRASES and lang in PHRASES[kind]:
                    G.add_edge(el, f"tr:{kind}:{lang}", rel="RENDERED_AS")
    return G


def artworks(G):
    return [n for n, d in G.nodes(data=True) if d["type"] == "artwork"]


def out_rel(G, node, rel):
    return [v for _, v, d in G.out_edges(node, data=True) if d["rel"] == rel]


def in_rel(G, node, rel):
    return [u for u, _, d in G.in_edges(node, data=True) if d["rel"] == rel]
