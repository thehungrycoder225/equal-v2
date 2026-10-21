"""Single-ad bias rules (Step 8).

Rule design follows the literature reviewed in literature-support-for-methods.md (Section 2.13):
 - explicit vs implicit separation, span-level evidence          (Frissen 2022; Everitt 2024; JABD taxonomy)
 - context check so descriptive mentions are not flagged        (Vethman 2022: "working with mostly male patients")
 - certainty field so unclear cases go to a human                (Havens 2022: uncertainty in annotation)
 - agentic / communal / balanced job label + "no_signal"        (Dikshit 2024, Gaucher 2011)
These are rules, not a trained model. Output is a set of flags with evidence for human review,
and must not be used to screen, rank or reject candidates.
"""
import re
from collections import Counter

RULES_VERSION = "step8-v1"

MASC = ("active adventurous aggress ambitio analy assert athlet autonom boast challeng compet confident "
        "courag decisive decision determin dominan driven fearless force headstrong hierarch impulsive "
        "independen individual intellect lead logic objective opinion outspoken persist self-relian "
        "self-sufficien stubborn superior unreasonab").split()
FEM = ("agree affectionate child cheer collab commit communal compassion connect considerate cooperat "
       "depend emotiona empath feel flatterable gentle honest interpersonal interdependen kind kinship "
       "loyal modest nurtur pleasant polite quiet respons sensitiv submissive support sympath tender "
       "together trust understand warm enthusias inclusive yield share").split()
FALSE_POSITIVE_PREFIXES = ("confidential", "committee", "shareholder", "kinds")
# Stems that in job ads usually describe duties, not personality
DUTY_PRONE = {"analy", "lead", "respons", "support", "decision", "commit", "connect", "understand", "share", "depend"}

# Standard-English gender terms. Filipino terms are an UNTESTED extension (no occurrence in the 1,500 ads).
MALE_TERMS = r"male|males|men|gentlemen"
FEMALE_TERMS = r"female|females|women|ladies"
MALE_FIL = r"lalaki|binata|kalalakihan"
FEMALE_FIL = r"babae|dalaga|kababaihan"
MALE_RE = re.compile(rf"\b(?:{MALE_TERMS}|{MALE_FIL})\b", re.I)
FEMALE_RE = re.compile(rf"\b(?:{FEMALE_TERMS}|{FEMALE_FIL})\b", re.I)
FIL_RE = re.compile(rf"\b(?:{MALE_FIL}|{FEMALE_FIL})\b", re.I)
INCLUSIVE_RE = re.compile(r"\b(?:either\s+gender|any\s+gender|regardless\s+of\s+(?:sex|gender)|men\s+and\s+women|"
                          r"gender\s*[:\-]?\s*(?:any|open|not\s+required))\b", re.I)
NOUN_RE = re.compile(r"\b(?:man|boys?|gentleman|woman|girls?|lady)\b", re.I)
NETWORK_RE = re.compile(r"\bWAN\b")  # "LAN, WAN, MAN": network type, not a gendered noun

# Vethman et al. (2022): a gender term can be descriptive ("mostly male patients") and not an eligibility rule
POPULATION = (r"patients?|clients?|inmates?|offenders?|prisoners?|detainees?|customers?|students?|pupils?|"
              r"residents?|children|kids|users?|members?|population|employees|staff|workforce|team|colleagues|co-workers")
DESCRIPTIVE_AFTER = re.compile(rf"^\W*(?:and\s+\w+\s+|or\s+\w+\s+)?(?:{POPULATION})\b", re.I)
DESCRIPTIVE_BEFORE = re.compile(r"(?:mostly|predominantly|mainly|majority|dominated\s+by|surrounded\s+by)\W+(?:\w+\W+){0,1}$", re.I)
ELIGIBILITY_CUE = re.compile(r"\b(?:only|preferably|preferred|must\s+be|should\s+be|applicants?|candidates?|needed|wanted|"
                             r"looking\s+for|required|requirement)\b", re.I)

TITLE_MALE = re.compile(r"\b(?:salesman|salesmen|houseboy|busboy|delivery\s+boy|utility\s+man|foreman|watchman|handyman|"
                        r"repairman|serviceman|chairman|businessman|cameraman|gentleman)\b", re.I)
TITLE_FEMALE = re.compile(r"\b(?:saleslady|salesgirl|sales\s+lady|waitress|stewardess|madam|maid|manicurist)\b", re.I)
PRONOUN_RE = re.compile(r"\b(?:he|she|his|him|hers)\b", re.I)

PROXIES = {
    "marital_status": re.compile(r"\b(?:single|married|unmarried|widow(?:ed|er)?|marital|pregnan\w*)\b", re.I),
    "age_limit": re.compile(r"\b(?:\d{2}\s*(?:-|to)\s*\d{2}\s*(?:years|yrs|yo|y/o|years\s+old)|"
                            r"(?:below|under|not\s+(?:more|older)\s+than|up\s+to|maximum\s+(?:age\s+)?of)\s*\d{2}|"
                            r"age[sd]?\s*(?:range|limit|requirement)?\s*[:\-]?\s*\d{2})\b", re.I),
    "appearance_physical": re.compile(r"\b(?:good\s+looking|pleasing\s+personality|presentable|attractive|"
                                      r"height|weight|physically\s+fit|heavy\s+lifting|tall|slim)\b", re.I),
}
# Exploratory classes (JABD marks young/old coded as exploratory; these lexicons are our own and unvalidated)
EXPLORATORY = {
    "young_coded": re.compile(r"\b(?:fresh\s+graduates?|young|youthful|energetic)\b", re.I),
    "disability_related": re.compile(r"\b(?:disabled|disability|handicap\w*|pwd|physically\s+challenged)\b", re.I),
    "nationality_related": re.compile(r"\b(?:filipino\s+citizen|citizen\s+of\s+the\s+philippines|nationality)\b", re.I),
    "religion_related": re.compile(r"\b(?:christian|muslim|catholic|religio\w*)\b", re.I),
}

SPLIT = re.compile(r"(?<=[.!?])\s+")


def split_units(text):
    out = []
    for line in str(text).split("\n"):
        line = re.sub(r"^\s*[•\-\*]\s*", "", line).strip()
        out += [p.strip() for p in SPLIT.split(line) if re.search(r"[A-Za-z]", p)]
    return out


def coded_words(text, stems):
    hits = []
    for w in re.findall(r"[a-z][a-z-]*", text.lower()):
        if w.startswith(FALSE_POSITIVE_PREFIXES):
            continue
        parts = [w] + (w.split("-") if "-" in w else [])
        matched = next((s for p in parts for s in stems if p.startswith(s)), None)
        if matched:
            hits.append((w, matched))
    return hits


def _term_matches(unit):
    """Gender-term matches in a unit, each labelled 'male'/'female' and descriptive or not."""
    res = []
    for side, rx in (("male", MALE_RE), ("female", FEMALE_RE)):
        for m in rx.finditer(unit):
            after = unit[m.end():m.end() + 40]
            before = unit[max(0, m.start() - 30):m.start()]
            desc = bool(DESCRIPTIVE_AFTER.match(after) or DESCRIPTIVE_BEFORE.search(before))
            res.append((side, m.group(0), desc))
    return res


def classify_unit(unit):
    """Return (type, certainty, descriptive_terms) for one sentence/line."""
    terms = _term_matches(unit)
    live = {s for s, _, d in terms if not d}
    descriptive = [t for _, t, d in terms if d]
    if INCLUSIVE_RE.search(unit) or live == {"male", "female"}:
        typ = "inclusive"
    elif live == {"male"}:
        typ = "restrictive_male"
    elif live == {"female"}:
        typ = "restrictive_female"
    else:
        return None, None, descriptive
    if typ == "inclusive":
        return typ, "definite", descriptive
    # Havens et al. (2022): record uncertainty instead of forcing a label
    short = len(unit.split()) <= 8
    certainty = "definite" if (short or ELIGIBILITY_CUE.search(unit)) else "uncertain"
    return typ, certainty, descriptive


def analyze_ad(text):
    """Analyse one job ad (raw masked text, cased, line breaks kept). Returns a dict of flags and evidence."""
    text = str(text or "")
    units = split_units(text)
    explicit, descriptive, uncertain_nouns, differentiated, co_occurrence = [], [], [], [], []
    for u in units:
        typ, cert, desc = classify_unit(u)
        if desc:
            descriptive.append({"sentence": u, "terms": desc})
        if typ:
            explicit.append({"sentence": u, "type": typ, "certainty": cert,
                             "taglish_term": bool(FIL_RE.search(u))})
            if typ == "inclusive" and MALE_RE.search(u) and FEMALE_RE.search(u) and re.search(r"\d", u):
                differentiated.append(u)
            if typ.startswith("restrictive") or typ == "inclusive":
                for k in ("marital_status", "appearance_physical", "age_limit"):
                    if PROXIES[k].search(u):
                        co_occurrence.append({"sentence": u, "with": k})
        elif NOUN_RE.search(u) and not NETWORK_RE.search(u):
            uncertain_nouns.append(u)
    types = [e["type"] for e in explicit]
    hm, hf = "restrictive_male" in types, "restrictive_female" in types
    direction = ("mixed_restrictions" if hm and hf else "male_restricted" if hm else
                 "female_restricted" if hf else "inclusive_only" if "inclusive" in types else "none")

    titles = [x.lower() for x in TITLE_MALE.findall(text) + TITLE_FEMALE.findall(text)]
    pronouns = [x.lower() for x in PRONOUN_RE.findall(text)]
    mh, fh = coded_words(text, MASC), coded_words(text, FEM)
    def tag(h, side):
        return [{"word": w, "stem": s, "side": side, "duty_prone": s in DUTY_PRONE} for w, s in h]
    coded = tag(mh, "masculine") + tag(fh, "feminine")
    m_core = sum(1 for w, s in mh if s not in DUTY_PRONE)
    f_core = sum(1 for w, s in fh if s not in DUTY_PRONE)
    proxies = {k: len(p.findall(text)) for k, p in PROXIES.items()}
    explor = {k: len(p.findall(text)) for k, p in EXPLORATORY.items()}

    def label(m, f):
        if m + f == 0:
            return "no_signal"
        return "agentic_masculine_coded" if m > f else "communal_feminine_coded" if m < f else "balanced"

    explicit_restrictive = direction in ("male_restricted", "female_restricted", "mixed_restrictions")
    title_pron = bool(titles or pronouns or uncertain_nouns)
    implicit_any = bool(coded or any(proxies.values()))
    if explicit_restrictive:
        category = "explicit_restrictive"
    elif title_pron:
        category = "explicit_title_or_pronoun"
    elif implicit_any:
        category = "implicit_only"
    elif direction == "inclusive_only":
        category = "inclusive_statement_only"
    else:
        category = "none_detected"
    needs_review = (category in ("explicit_restrictive", "explicit_title_or_pronoun")
                    or any(e["certainty"] == "uncertain" for e in explicit)
                    or bool(descriptive) or bool(co_occurrence))
    return {
        "rules_version": RULES_VERSION,
        "n_words": len(text.split()), "n_units": len(units),
        "explicit": {"direction": direction, "spans": explicit, "titles": titles, "pronouns": pronouns,
                     "bare_gendered_nouns": uncertain_nouns, "descriptive_mentions": descriptive,
                     "gender_differentiated_requirements": differentiated,
                     "gender_with_proxy": co_occurrence},
        "implicit": {"coded_words": coded, "masc_hits": len(mh), "fem_hits": len(fh),
                     "core_masc_hits": m_core, "core_fem_hits": f_core, "proxies": proxies, "exploratory": explor},
        "job_label": label(len(mh), len(fh)), "job_label_core": label(m_core, f_core),
        "bias_category": category, "needs_human_review": needs_review,
    }


def summarise(result):
    """Plain-text summary of analyze_ad() output with the evidence that triggered each flag."""
    e, i = result["explicit"], result["implicit"]
    lines = [f"Category: {result['bias_category']} | job label: {result['job_label']} | review: {result['needs_human_review']}"]
    lines.append(f"Explicit direction: {e['direction']}")
    for s in e["spans"]:
        lines.append(f"  - [{s['type']}, {s['certainty']}] {s['sentence']}")
    for k in ("titles", "pronouns", "bare_gendered_nouns", "gender_differentiated_requirements"):
        if e[k]:
            lines.append(f"  - {k}: {e[k]}")
    for d in e["descriptive_mentions"]:
        lines.append(f"  - descriptive mention (not flagged as a requirement): {d['sentence']}")
    for c in e["gender_with_proxy"]:
        lines.append(f"  - gender stated together with {c['with']}: {c['sentence']}")
    if i["coded_words"]:
        lines.append("  - coded words: " + ", ".join(f"{c['word']}({c['side'][0]}{'*' if c['duty_prone'] else ''})" for c in i["coded_words"])
                     + "   (* = often a duty word)")
    pr = {k: v for k, v in {**i["proxies"], **i["exploratory"]}.items() if v}
    if pr:
        lines.append(f"  - proxies/exploratory: {pr}")
    return "\n".join(lines)
