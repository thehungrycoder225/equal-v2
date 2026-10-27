# Annotation Guidelines v0.2 — Explicit and Implicit Gender Bias in PESO Job Advertisements

**Status:** decisions D1–D5 applied as approved (see §6). Not yet tested by any annotator. No labels exist yet.
**Scope:** gender bias only (explicit and implicit). Age, ethnicity, religion and disability are out of scope.
**Unit of annotation:** the sentence/requirement units in `outputs/analysis/units.csv` (7,971 units, 1,500 ads). Each annotation is a span stored with the unit's `unit_id` and character offsets, so it can be traced to the raw ad.

---

## 1. Source and what was adopted

The reference is *Annotation Guidelines: Bias in Job Advertisement* (Bórquez and Mendoza; https://borquezmartin.github.io/job-ad-bias-annotation-guide/), read for the sections Summary, Explicit Gender Bias, Implicit Gender Bias, Polisemantic Class, Others Class and Examples. Rules below are adopted from it unless marked **[EXT]** (our extension) or **[DEC]** (a decision needing your approval).

Adopted from the reference:

| # | Rule in the reference | Use here |
|---|---|---|
| A1 | The task is token/span-level. Annotators highlight words or phrases carrying bias, with the full ad available for context. | Same. Context = the full ad plus neighbouring units. |
| A2 | Work flows pre-annotation (lexicon) → human curation. Lexicons are incomplete because they ignore sentence structure and context. | Same. Our rules (Step 8e) give pre-annotations; the annotator accepts, rejects or relabels each. |
| A3 | Categories are mutually exclusive and should not overlap. | One label per span. |
| A4 | Mark the longest continuous phrase that conveys the bias (their example: "physical disability", not "disability"). | Same. See §4 for how this applies to restriction lines. |
| A5 | If two words of the same category each qualify on their own and sit close together, annotate them separately. | Same. |
| A6 | Bias is conceptualised as language that affects how a job is perceived by people with a protected attribute. It can be unconscious and does not always imply discrimination. | Same. This is why "implicit" is not a legal judgement. |
| A7 | Explicit gender bias = Gender Exclusionary Terms (Explicit Marking of Sex, Gendered Neologism) and Generic Pronouns (Generic He, Generic She). Implicit gender bias = Gendered Stereotypical Terms (Masculine Coded, Feminine Coded). | Same families. Gendered titles are placed under explicit (E2), as in the reference (D2). |
| A8 | Generic He/She is judged at sentence level, because it depends on context. A named, sex-definite person ("David… He manages…") is not generic. | Same. |
| A9 | Polisemantic: words that are neutral in this job-ad context but could convey bias elsewhere. Annotators flag them even without a lexicon match and confirm the neutral use. | Same. |
| A10 | Others: bias that fits no category, including intersectional terms and new patterns. Flag for later review. | Same. |

Caveats on the reference:
- The released JABD annotation file labels gender tokens with the coarse tag `Gender`, so the fine classes cannot be checked from the data. The fine classes come from the guide text.
- In the JABD data, "male" and "female" tokens carry `Gender` in 17 of 17 and 17 of 20 occurrences, so those words are treated as gender bias there, although the guide has no named class for a "Female only" requirement line. That gap is what E1 below fills.
- The agreement figures I read earlier from the JABD README were moderate (Krippendorff α about 0.52). Adopting the definitions does not make our labels reliable; reliability must be measured on our own annotators.
- I could not find the "243 annotators / 100 items each" description in the README or repository (see the audit trail). The number 243 does appear in the JABD file as the count of rows with `annotation_type = Preannotation Confirmed`; I have not established any link to your description.

---

## 2. Label set

Each span receives exactly one label.

### Explicit gender bias

| Code | Label | Definition | Origin |
|---|---|---|---|
| **E1** | Gender Restriction / Preference | A stated requirement or preference for one gender: "Female", "Male only", "Preferably male". | **[EXT]** |
| **E2** | Explicit Marking of Sex | A gender-neutral job or role named with a word that denotes one gender: -man, -woman, -lady, -boy titles. | Reference |
| **E3** | Gendered Neologism | A newly coined gender-specific term. | Reference |
| **E4** | Generic He | A male pronoun for a sex-indefinite role. | Reference |
| **E5** | Generic She | A female pronoun for a sex-indefinite role. | Reference |

### Implicit gender bias

| Code | Label | Definition | Origin |
|---|---|---|---|
| **I1** | Masculine Coded | Wording associated with male stereotypes in work recruitment, e.g. competitive, aggressive. | Reference |
| **I2** | Feminine Coded | Wording associated with female stereotypes, e.g. supportive, nurturing, family-friendly. | Reference |

### Other labels

| Code | Label | Definition | Origin |
|---|---|---|---|
| **INC** | Inclusive | Wording that names more than one gender or welcomes all genders, so that no gender is excluded or preferred: "Female/Male", "Male or Female", "M/F", "He/She". Not bias. | **[EXT]** (D3) |
| **P** | Polisemantic | A word that matches a gender cue but is neutral here (see §3). | Reference |
| **O** | Others | A gender-related bias that fits nowhere above, or a term fitting two categories. | Reference |

A unit with no span has no gender bias. Bias presence is derived from the labels: E1–E5 are explicit and I1–I2 are implicit. INC and P are not bias. O is not counted as bias until it has been reviewed and re-labelled or confirmed. Rewrite is not needed for INC.

---

## 3. Decision rules

**Step 1.** Read the unit, its neighbours and the ad. Review each pre-annotated span: accept, reject, or relabel. Then add spans the rules missed.

**Step 2.** For each span choose the first rule that fits.

1. A gender word states who may or should apply (male, female, men, women, lalaki, babae as a requirement) → **E1**.
2. A role or job title is built with a gendered word (foreman, salesman, watchman, saleslady, farm boy) → **E2**.
3. A male or female pronoun refers to a role, not to a named person → **E4 / E5**. "He/She" or "his/her" together is not E4 or E5; label it **INC**. A line that lists both genders but still restricts, for example "Male or Female, must be single", keeps INC for the listing; put the other requirement in `notes`.
4. A word or phrase carries a masculine or feminine work stereotype (see I1/I2 lists below) and is used to describe the candidate, team or culture → **I1 / I2**.
5. The word matches a cue but the context is neutral → **P**.
6. The case fits nothing above, or fits two → **O**, with a note.

### Coded wording (I1, I2)
- Mark the phrase that carries the coding. The reference marks short phrases ("eye for detail", "family-friendly environment") and not just single words.
- The pre-annotation lexicon follows Gaucher et al. (2011) (agentic = masculine coded, communal = feminine coded). Keep the lexicon as a prompt; the annotator decides from context.
- Words that name a job or duty are **P**, not I1/I2. In our rule output, the matched words with the highest counts include `analyst` (23), `analysis` (25), `support` (43), `leader` (15) and `understand` (16). Examples of P: "Business Analyst" as a title, "technical support" as a department. Example of I1: "assertive, competitive" describing the candidate.

### Polisemantic (P) examples from our rule output
- "Ms. Mary Claire Limpiada (Owner)" in an instruction to send a message: an honorific for a named contact person, not a requirement.
- "analyst", "support", "leader" when they name a role.

### Others (O)
Use for gender-differentiated requirements that are not a restriction, for example a height requirement given "for Male" and "for Female" separately (row-0109-s011), or "must not be pregnant" (row-0025-s006, with the gender span itself labelled separately as E1). Also use O for intersectional terms. Non-gender biases (age, marital status, religion) are not labelled here: record them in `notes`.

---

## 4. Span rules for our units

- **Span = the gender-bearing words**, copied from the unit, not the whole line. "Female SRs must not be pregnant" → span "Female"; the rest is described in `notes`. "Preferably Male" → the whole phrase "Preferably Male", because the preference wording is part of the restriction (A4).
- Job titles are whole units, but the span is only the gendered word: "Foreman Civil" → "Foreman".
- Spans never cross units. Offsets are relative to the unit text and are converted to raw offsets with the unit's `char_start` and `mask_edits`.
- Placeholders `[EMPLOYER]`, `[EMAIL]`, `[URL]` and `[PHONE]` are never part of a span.
- Filipino/Taglish wording is labelled with the same rules; set `filipino_taglish` in `notes`.

---

## 5. Review workflow (matches the reference figure)

Pre-annotation → annotator decision per span (**accepted / rejected / relabelled / added**) → curation by a second annotator → adjudicated label. Every status change keeps the previous label, so the history of the span stays visible (for example a span pre-annotated as I1 and relabelled P).

Rewrite is a separate, optional field and is not part of the bias label: suggest a neutral replacement for the span only, leaving the job's real requirements unchanged.

---

## 6. Decisions (approved)

D1, D2, D4 and D5 were approved as proposed. D3 was approved with a change: the listing label is **Inclusive (INC)** and is not counted as bias.

| ID | Question | Evidence | Decision |
|---|---|---|---|
| **D1** | Add E1 Gender Restriction/Preference as a label of our own. | The reference has no class for requirement lines such as "Female". In our Step 8e output 306 rows (15 distinct sentences) are restriction and 15 rows (7 distinct sentences) preference; the explicit class is almost entirely this type. | Yes. Without it, the commonest explicit pattern in PESO would be forced into O. |
| **D2** | Gendered titles (foreman, salesman, watchman): explicit (E2) or implicit? | The reference lists Explicit Marking of Sex under Explicit Gender Bias. Step 8e labelled titles *implicit* (37 rows; foreman 22, salesman 13, watchman 1, saleslady 1). | Explicit (E2), to follow the reference. This changes the earlier Step 8e label and Step 8h targets. |
| **D3** | How to treat "Female/Male" and "Male or Female" (99 rows in Step 8e). | The reference has no equivalent class. The listing names both genders and excludes none. | **Changed by you:** label as Inclusive (INC); not bias; no rewrite needed. |
| **D4** | Honorifics ("Ms.", "Mr.") for contact persons. | 7 of the 14 distinct "unclear" sentences in Step 8e (11 of 27 rows) are "Ms." matches; the rest are "male", "female" or "man" in sentences the rules could not classify. | Label as P, not bias. |
| **D5** | Gender-differentiated requirements (height/weight by gender) and pregnancy. | One example found (row-0109-s011) plus row-0025-s006. | Label the gender span if it is a restriction; otherwise O with a note. |

---

## 7. Known problems in the pre-annotation (for annotators to catch)

These are observed, not fixed; the rules were not changed.
- row-1416-s005 "Knowledge in computer operation preferably MS Excel…": the preference rule matched "preferably MS". This is not gender; reject.
- Honorific matches ("Ms.") on contact instructions are flagged as `unclear` by the rules; label P.
- Coded-wording matches on role nouns (analyst, analysis, support) are frequent; label P where they name a role.
- Pre-annotations are silver (rule-based). Scores against them measure rule reproduction, not validity.

---

## 8. What this version does not do

- It has not been piloted. Items such as how annotators treat INC and P cannot be known until two people use it.
- No agreement statistic exists for it.
- It does not replace the earlier `step8i_annotation_guidelines.md` (v0.1) or the Step 8i workbooks, which are keyed to the old unit file and the Layer A fields.
