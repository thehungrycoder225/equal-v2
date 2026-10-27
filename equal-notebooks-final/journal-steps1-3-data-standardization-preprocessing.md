# Steps 1–3: Data Standardization and Preprocessing — Method Journal

*Draft for review. Source notebook: `equal-s1-3-data-standardization-preprocessing.ipynb`. All figures below are taken from its executed output.*

## Draft discussion (manuscript text)

We prepared the analysis text in two stages. First, a rule-based parsing procedure separated each advertisement into employer name, job title, qualification text, other body text, contact/application information, and source URL. We created a masked analysis version to reduce direct employer and contact identifiers in model-facing text. Employer names and recognized variants, contact/application information, and source URLs were kept separately from the analysis text. Employer names repeated within retained text were replaced with [EMPLOYER]; e-mail addresses, URLs, and phone-like strings found in retained text were designated for replacement with [EMAIL], [URL], and [PHONE]. The contact/application field itself was excluded from the modeling text and represented as [CONTACT].

For finer-grained review, we generated sentence-/requirement-level units from the parsed dataset. Job titles were kept as whole units; body and qualification text were segmented at line or bullet boundaries and, where appropriate, at sentence-ending punctuation. Each unit was linked to its source advertisement and component, as job advertisements are written in fragments or bullets and describe requirements rather than grammatical sentences. Each unit also records the character span it occupies in the unmodified advertisement, so that any later label or edit can be traced to the original wording. Normalization (lowercasing and whitespace standardization) was applied as a length-preserving view of each unit, so that character positions are identical in the masked and normalized text.

```
[job_title]  Cashier
[qualification]  Female
[qualification]  Graduate of any 4-year course or at leasr 2 years in college
[qualification]  With pleasing personality
[qualification]  With or without experience
```

**Figure x:** Example of sentence-/requirement-level data (advertisement `row-0038`). Text is shown as it appears in the source, including the source spelling "leasr".

## Results reported by the notebook

| Measure | Value |
|---|---:|
| Advertisements | 1,500 |
| Non-empty source lines | 14,819 |
| Lines assigned to employer name / job title | 1,500 / 1,497 |
| Lines assigned to qualification (header-only lines excluded) | 6,281 |
| Qualification header-only lines | 1,347 |
| Lines assigned to other body text | 96 |
| Lines assigned to contact/application | 4,098 |
| Advertisements with contact/application lines | 1,218 |
| Advertisements with a source URL | 1,499 |
| Sentence-/requirement-level units | 7,971 (job title 1,497; body 100; qualification 6,374) |
| Advertisements with `[EMPLOYER]` in retained units | 16 |
| Retained units with `[EMAIL]`, `[URL]` or `[PHONE]` | 0 |
| Advertisements flagged `no_title` / `no_qualification_block` | 3 / 157 |

Because contact lines are routed out of the analysis text during parsing, no e-mail, URL or phone-like string remained in retained text to be replaced; the manuscript sentence above should be read as the rule that was applied, not as a count of replacements.

## Method notes

1. **Raw layer.** The text of each advertisement is read exactly as supplied and fingerprinted (SHA-256). It is never edited. The base workbook has no carriage returns, no Unicode NFC changes, no length-changing lowercase characters, and none of the private-use character used internally by the segmenter (all counted in the notebook).
2. **Parsing.** The rules are those of the earlier Step 1 (first non-empty line = employer; following short non-bullet line = title; one top-to-bottom pass with the state body → qualification → contact). Each non-empty line receives exactly one component and a rule name, and keeps its character span in the raw text.
3. **Masking with offsets.** Masking is applied to each component block, as in the earlier Step 2, so a name that wraps across two lines is still masked. Each masked character keeps a pointer to the raw interval it came from; a placeholder points to the whole raw string it replaced. Each unit stores `mask_edits` (`[raw_start, raw_end, placeholder]`).
4. **Segmentation.** Rules unchanged from the earlier Step 2: job titles whole; line/bullet boundaries; splitting at `.`/`!`/`?` followed by whitespace; periods in decimals, dotted initials, common abbreviations and numbered-list markers protected; units without a letter skipped; leading list marker excluded from the unit span.
5. **Normalization view.** `text_norm` = masked text with each whitespace character replaced by a space and letters lowercased. No characters are added or removed, no words are filtered, punctuation is kept.
6. **Separation of files.** Raw text, employer name, contact lines and source URL are written only to `outputs/RESTRICTED_raw_and_contact/raw_layer.csv`. The files under `outputs/analysis/` contain no raw-text, employer-name, contact or source-URL column.

## Validation (automatic, from the notebook)

All 12 checks passed: raw text identical to a fresh read; every non-empty line has exactly one component (14,819 of 14,819); raw span plus `mask_edits` reproduces the masked text of every unit (0 mismatches); units without placeholders equal `raw[char_start:char_end]`; units are non-empty, ordered and non-overlapping; unit IDs unique; `text_norm` has the same length as `text_masked`; no e-mail/URL/phone-like string and no employer name in unit text; analysis tables carry no raw/employer/contact/source column; and a span mapped through placeholders returns to the correct raw interval (16 units tested, 0 failures).

**Consistency with the earlier pipeline.** All 7,971 units and unit IDs coincide with the earlier `step2_masked_sentence_units.csv` (7,971 of 7,971 text and component matches after whitespace collapsing), so existing unit IDs remain valid.

## Limitations to state

- Parsing, masking and segmentation are rule-based and were not scored against human-labelled ground truth; the checks above test internal consistency and traceability, not parsing accuracy.
- Employer masking removes the stated name and its suffix-free form only; other wording that could identify an employer is not removed.
- The employer is a positional rule (first non-empty line); the 3 advertisements with no title and the 157 with no qualification block are flagged for human review.
- Units record only the part of a line after the list marker; header-only qualification lines (1,347) and contact lines carry no unit.
