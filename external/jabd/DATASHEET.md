# Datasheet for JABD (Job Advertisements Bias Dataset)

Following Gebru et al., *Datasheets for Datasets* (2021).

Figures below were recomputed from the released file, not copied from the paper.

---

## Motivation

**For what purpose was the dataset created?**
To enable the study and automatic detection of linguistic bias in job advertisements at the level
where it actually occurs — the word and the phrase. Existing resources annotate whole postings or
whole sentences, which tells you *that* an ad may be biased but not *which* expression makes it so.
JABD was built to make bias traceable to specific spans, so that detections can be reviewed,
contested and revised by a human.

**Who created it and who funded it?**
Martín Bórquez, Marcelo Mendoza, Vicente Lavagnino and Gonzalo Valdés (School of Engineering,
Pontificia Universidad Católica de Chile).

Funding: ANID Fondecyt grant 1241462.

---

## Composition

**What do the instances represent?**
Each instance is one sentence extracted from a real job advertisement, tokenised and labelled with
BIO tags at four levels of a bias taxonomy.

| | |
|---|---|
| Instances (sentences) | 14,960 |
| Source advertisements | 8,993 |
| Tokens | 418,069 |
| Flagged spans | 34,598 |
| Leaf classes | 12 |

**Does each instance consist of "raw" data?**
Tokens are lemmatised and lowercased, not verbatim ad text. The complete advertisement text is
**not** included — see *Distribution*.

**Is any information missing?**
Yes, and deliberately: the `ad` and `ad_annot` columns of the internal working file, which held
the full source advertisement, are removed. `scripts/rehydrate_from_emscad.py` restores them for
users who hold EMSCAD.

Beyond that, no column is empty, but seven are populated only for the rows where they mean
something. This follows from the annotation design rather than from data loss, and it is worth
knowing before you filter on any of them:

| Column | Rows | Populated for |
|---|---:|---|
| `annotation_time_seconds` | 13,244 | `Single Review` only. Consolidated rows are a merge of several passes and gold-standard rows were built by the team, so neither has a single elapsed time. |
| `n_annotators` | 1,323 | `Consolidated Review` only, the rows that more than one annotator saw. Elsewhere the count is one by construction. |
| `krippendorff_alpha` | 1,292 | `Consolidated Review`, minus 31 rows where agreement was not computable. |
| `span_agreement`, `recall_sp`, `balanced_accuracy` | 13,487 | `Single Review` and `Preannotation Confirmed`. These describe *the annotator*, measured on the gold standard and attached to every row they produced, so they are absent where a row has no single author: consolidated and gold-standard rows. |
| `location` | 14,755 | Wherever the source advertisement carried one; 205 do not. |

The remaining 22 columns are populated for all 14,960 rows.

**Are there labels?**
Yes. `labels` holds leaf-level (L4) BIO tags; `token_labels1`–`token_labels4` project the same
spans onto the four taxonomy levels. Two auxiliary annotation classes, *Polysemantic* (looks
biased out of context but is not) and *Others* (bias not yet in the taxonomy), were available to
annotators to reduce forced-choice errors.

**Class distribution**

| Class | Group | Type | Spans |
|---|---|---|---:|
| Masculine Coded | Gender | implicit | 10,768 |
| Feminine Coded | Gender | implicit | 8,193 |
| Nationality Related | Ethnicity | explicit | 4,208 |
| Young Coded \* | Age | implicit | 2,190 |
| Age Related | Age | explicit | 1,986 |
| Ethnic Related | Ethnicity | explicit | 1,513 |
| Disability | Disability | explicit | 1,462 |
| Old Coded \* | Age | implicit | 1,124 |
| Explicit Marking of Sex | Gender | explicit | 957 |
| Generic He | Gender | explicit | 795 |
| Religion | Religion | explicit | 761 |
| Generic She | Gender | explicit | 641 |

\* Exploratory — see *Recommended uses*.

The distribution is heavily imbalanced: the two coded-gender classes alone account for 55% of all
spans, because the pre-annotation lexicon is densest there. Do not read span frequency as
prevalence of bias.

**Are there errors, sources of noise, or redundancies?**
Yes, and they are measured rather than merely acknowledged.

*Inter-annotator agreement.* Krippendorff's α was computed on the multiply-annotated subset
(≈8.6% of the corpus); overall α = 0.52. Per class:

| Class | α | | Class | α |
|---|---:|---|---|---:|
| Disability | 0.71 | | Age Related | 0.37 |
| Generic She | 0.60 | | Feminine Coded | 0.36 |
| Religion | 0.55 | | Ethnic Related | 0.44 |
| Explicit Marking of Sex | 0.54 | | Old Coded | 0.40 |
| Nationality Related | 0.48 | | Masculine Coded | 0.23 |
| Generic He | 0.39 | | Young Coded | 0.22 |

The ordering is the important part: explicit, lexically anchored categories are reliable;
implicit "Coded" categories are not. Treat a *Masculine Coded* or *Young Coded* label as a weak
signal, not a fact.

*Lexicon seeding.* Pre-annotation was lexicon-seeded, so labels partly reflect the seed lexicon's
coverage. A term absent from the lexicon is less likely to have been flagged at all. This is the
main reason the coded-gender classes dominate the span counts.

*Precision of the lexical signal outside the source period.* 500 lexicon matches drawn from a
2020–2023 recruitment corpus (50 per category) were judged in context by a human; 259 were
confirmed as genuine bias, 204 as not. Overall precision 55.9%, but strongly category-dependent:

| Category | Precision | | Category | Precision |
|---|---:|---|---|---:|
| Explicit Marking of Sex | 91.8% | | Nationality Related | 52.1% |
| Disability | 86.0% | | Feminine Coded | 35.4% |
| Generic He | 76.0% | | Ethnic Related | 28.6% |
| Age Related | 73.7% | | Masculine Coded | 27.7% |
| Religion | 71.1% | | Generic She | 10.3% |

*Generic She* is largely lexicon noise: the feminine generic appears almost only inside inclusive
"he/she" constructions. Some *Disability* and *Religion* matches are equal-opportunity statements
counted as mentions. Do not read a match as evidence of exclusion.

*Mention is not hostility.* The taxonomy records that a protected attribute is **invoked**, not
that the usage is hostile. Inclusive and equal-opportunity statements are flagged too. Valence is
left to the reader.

**Is the dataset self-contained?**
The annotation layer is. The source text depends on EMSCAD, obtained separately.

**Does it contain data that might be offensive?**
The corpus is drawn from ordinary recruitment advertising, but by construction it concentrates
language that references gender, ethnicity, age, religion and disability, and some of it is
exclusionary.

**Does it identify subpopulations / contain data that could identify individuals?**
The annotated sentences are advertisement text, not personal data about applicants. Source
advertisements do contain employer contact details; those live in the full-text columns that are
**not** distributed here. Annotator identifiers are pseudonymous.

---

## Collection

**How was the data acquired?**
Sentences were drawn from EMSCAD (Employment Scam Aegean Dataset), 17,014 genuine English-language
advertisements published 2012–2014, released by the University of the Aegean to support research
on recruitment fraud. Text was segmented by section then by sentence, POS-tagged and lemmatised
with NLTK.

**Sampling strategy**
Not a uniform sample. Sentences were prioritised by lexicon pre-annotation, so the corpus is
enriched for bias-bearing language relative to a random sample of recruitment text. **This makes
JABD unsuitable for estimating how frequent bias is in job advertising at large.**

**Who was involved and how were they compensated?**
243 annotators were recruited via Prolific and screened for professional English proficiency. 194
distinct annotator identifiers appear in the released data after quality filtering on
specialisation recall and balanced accuracy. Each reviewed 100 items: 15 blinded gold-standard
items and 85 stratified samples.

The pool was gender-balanced (51.05% male, 48.95% female), spanned more than 25 nationalities and
ages 19–67 with most between 25 and 40, and the large majority reported English as a first
language.

Annotators were compensated according to the protocol established by Prolific, the platform
through which they were recruited.

**Over what timeframe was the data collected?**
Source advertisements were published 2012–2014. The annotation campaign ran between June and July
2025. Note the gap: the language annotated here predates the widespread adoption of inclusive
recruitment wording, which is why such wording is underrepresented (see *Discouraged / out of
scope*).

**Were ethical review processes conducted?**
Yes. The project was approved by the Institutional Review Board of the Pontificia Universidad
Católica de Chile (protocol no. 230614033), under ANID Fondecyt grant 1241462.

---

## Preprocessing / labelling

Four phases: (1) sentence segmentation and lemmatisation; (2) lexicon-based pre-annotation
flagging candidate spans; (3) human review, in which annotators saw the target sentence, the
pre-annotations and the full advertisement for context, with the annotation guide always
available; (4) consolidation, resolving multiply-annotated sentences by intersection — the rule
that scored best in F1 against the gold standard.

Annotators were trained and evaluated per specialisation class against a 150-item gold standard
(120 biased, 30 non-biased, of which 24 are near-miss counterexamples).

The annotation guide is published at
<https://borquezmartin.github.io/job-ad-bias-annotation-guide/>.

---

## Uses

**Recommended**
- Training and evaluating token- or span-level bias detection (NER-style).
- Studying how detectability varies by bias category and by annotation reliability.
- Auditing a draft advertisement to surface expressions for **human** review.

**Report benchmarks over the ten core classes.** *Old Coded* and *Young Coded* should be treated
as exploratory: they carry no confirmed pre-annotations, have the smallest consolidated support of
any class (13 and 14 spans), and the lowest agreement. Including them depresses macro-F1 by
roughly 9–11 points for every encoder and says more about label noise than about model quality.

**Discouraged / out of scope**
- Automated screening, ranking, rejection or any other decision about a person. The resource
  flags *language*, never a candidate.
- Legal or compliance determinations. A flag is not a finding of discrimination.
- Estimating population-level prevalence of bias (see *Sampling strategy*).
- Transfer to other languages, sectors or periods without revalidation. Bias expression is
  culturally contingent; on a 2020–2023 recruitment corpus the taxonomy's lexical signals remain
  frequent but their precision is strongly category-dependent.

---

## Distribution

Distributed through GitHub and archived on Zenodo with a DOI. The annotation layer is released;
the source advertisement text is not (see the README).

**Licence:** JABD Open RAIL-D — an adaptation for a data artifact of the Open RAIL family
published by the Responsible AI Licenses initiative, following the structure of CreativeML Open
RAIL-M. Access, reuse, modification and redistribution are permitted free of charge, including
commercially, provided the use restrictions in Attachment A travel with every copy and every
derivative — including models trained on the data. The restrictions prohibit, among other things,
using the resource to make or assist decisions about identified people, to compose exclusionary
recruitment language or evade bias detection, to infer protected attributes, or to present an
automated output as a legal determination. See `LICENSE` for the full text.

Zenodo has no OpenRAIL entry in its licence vocabulary, so the deposit records "Other
(Attribution)" and points to `LICENSE` for the operative terms. It is deliberately not recorded as
"Other (Open)": a licence with use restrictions is not open in the Open Definition sense.

---

## Maintenance

**Who maintains it and how can they be contacted?**
Marcelo Mendoza (corresponding author), <marcelo.mendoza@uc.cl>. Issues may also be opened on the
GitHub repository.

**Will it be updated?**
Corrections and extensions are expected, in particular a stronger treatment of implicit age bias
and coverage of inclusive language, which is underrepresented because the source corpus predates
its widespread adoption. Versions are tagged and each release receives its own DOI.

**Will older versions remain available?** Yes — Zenodo records are permanent.

**How can others contribute?** Via issues and pull requests on the GitHub repository.
