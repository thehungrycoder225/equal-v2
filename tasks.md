# Project tasks

Last updated: 2026-10-24. Status is based on files in this repository. Pending items need your approval before work starts.

## Done

| # | Task | Evidence |
|---|---|---|
| 1 | Step 1 structural parsing, reviewed, no change needed | `equal-step1-structural-parsing.ipynb` |
| 2 | Step 2 masking and canonical sentence segmentation (7,971 units from 1,500 ads) | `equal-step2-masking.ipynb`, `outputs\equal_step2_masking\` |
| 3 | Step 4 sentence embeddings, recalibrated to the Step 2 units | `equal-step4-sentence-embeddings.ipynb` |
| 4 | Steps 6 and 7 job-level labelling, recalibrated | `equal-step6-bias-analysis.ipynb`, `equal-step7-job-level-embedding.ipynb` |
| 5 | Step 8 annotation schema and 596-unit stratified sample (IAA skipped by decision) | `equal-step8-annotation-schema.ipynb` |
| 6 | Literature search and citation validation; M13 and [25]-[34] added | `literature-support-for-methods.md` |
| 7 | Step 9 silver-label baseline classifier (not validated against human labels) | `equal-step9-silver-baseline-classifier.ipynb` |
| 8 | Step 9 section 9: bias detection test for a single ad and multiple ads | same notebook, cells 17-22 |
| 9 | Step 10 rewrite baseline for explicit bias (rules; no human evaluation) | `equal-step10-rewrite-baseline.ipynb`; literature M14 added |
| 10 | Step 11 prompted LLM rewrite for appearance lines, with guardrail checks (no human evaluation) | `equal-step11-llm-rewrite.ipynb`; literature M15 added |
| 14 | Step 13 gender-bias detector retrained on PESO silver labels with detection, explicit/implicit and span metrics (rule reproduction, not validated) | `equal-step13-gender-detector.ipynb` |
| 15 | Step 8d class-wise comparison of Layer B explicit/implicit rules with JABD's human-annotated gender labels; taxonomy mismatch documented | `equal-step8d-jabd-schema-crosswalk.ipynb`, `outputs\equal_step8d_jabd_schema_crosswalk\` |
| 16 | Step 9B Layer B-aligned silver classifier added alongside, not over, the legacy Step 9 baseline; unclear units excluded, employer-grouped CV and class-weight comparison run | `equal-step9b-layerB-silver-classifier.ipynb`, `outputs\equal_step9_layerB_silver\` |
| 17 | Step 8e Layer A lexicons/patterns applied across PESO to produce reference, restriction/preference, coded-expression and span-level silver annotations; no human validation | `equal-step8e-layerA-rule-detection.ipynb`, `outputs\equal_step8e_layerA_rule_detection\` |
| 18 | Step 8f Explicit Age Bias rule pre-annotator (silver) on PESO and scored vs JABD `Age Related`; JABD README/experiments repo reviewed (243/100-item annotation claim not found in either) | `equal-step8f-explicit-age.ipynb`, `outputs\equal_step8f_explicit_age\` |
| 19 | Step 8g base-dataset re-analysis (xlsx), preprocessing check, and PESO frequency + JABD scoring for ethnicity/nationality, religion, disability (silver rules) | `equal-step8g-category-screening.ipynb`, `outputs\equal_step8g_category_screening\` |
| 20 | Step 8h Layer A multi-label gender detector (gender reference / restriction-preference / coded wording) on Step 8e silver labels: minimal-normalisation TF-IDF vs frozen DistilBERT (max_length 128), nested employer-grouped CV, raw/masked/deleted-span leakage guards | `equal-step8h-layerA-detector.ipynb`, `outputs\equal_step8h_layerA_detector\` |
| 21 | Step 8i gold-sample annotation kit: 250 distinct-text stratified sample, blind annotator A/B workbooks, adjudication template, guidelines, hidden rule key, agreement/span-score helpers (annotation itself pending) | `equal-step8i-gold-sample-kit.ipynb`, `outputs\equal_step8i_gold_sample_kit\` |
| 22 | Steps 1-3 data standardization and preprocessing redone offset-preserving in a new folder: raw layer, line table with raw spans, masked units with raw char_start/char_end and mask_edits, length-preserving normalization view, 12 validation checks passed, 7,971/7,971 units match legacy Step 2 IDs; method journal drafted (awaiting review) | `equal-notebooks-final\equal-s1-3-data-standardization-preprocessing.ipynb`, `equal-notebooks-final\journal-steps1-3-data-standardization-preprocessing.md`, `equal-notebooks-final\outputs\` |
| 23 | Gender annotation guidelines v0.2: reference guide (Bórquez and Mendoza) explicit/implicit gender sections reviewed, adopted rules vs own extensions separated, five decisions (D1-D5) proposed; not piloted, no labels | `equal-notebooks-final\annotation-guidelines-gender-v0.2.md` |
| 24 | Step 4 (final folder): gender annotation schema v0.2 in machine-readable form plus crosswalk of the 1,218 Step 8e silver span rows to v0.2 candidate labels with raw offsets; separate from older Step 8 notebooks; no human labels, no training | `equal-notebooks-final\equal-s4-gender-annotation-schema-v0.2.ipynb`, `equal-notebooks-final\outputs\s4_schema_v0.2\` |
| 13 | Step 8c Layer B definition and design test (rule pre-annotation, JABD gender-only check); no human labels | `equal-step8c-layerB-test.ipynb` |
| 12 | Step 8b gender-focused Layer A annotation schema and validator (labels empty; Layer B pending) | `equal-step8b-gender-schema.ipynb` |
| 11 | Step 12 external validation on JABD (human-annotated) in place of PESO human labels; label-definition mismatch found | `equal-step12-jabd-validation.ipynb`; data in `external\jabd\` |
| 25 | Final folder, Steps 4b-9: taxonomy v0.3 overlap test (6 decisions still open); Step 5 pre-annotation, 5a analysis, 5b v0.3 re-expression; Step 6 DistilBERT tagger; Step 7 explicit detection (lexicon vs RoBERTa); Step 8 implicit detection (TF-IDF vs DistilBERT); Step 9 neutral rewriting (rules, t5-small, Qwen2.5-1.5B, cascade; automatic metrics only). All silver labels, no human labels | `equal-notebooks-final\equal-s4b-*`, `equal-s5*`, `equal-s6*`, `equal-s7-*`, `equal-s8-*`, `equal-s9-neutral-rewriting-module.ipynb`; see `audit-trail.md` |

## Pending (not started, awaiting approval)

| # | Task | Notes |
|---|---|---|
| P1 | Human-label the 596-unit Step 8 sample | Deferred for time. Step 12 and Step 8d compare against JABD, but neither validates the PESO silver labels or agreement among annotators using our schema. |
| P2 | Step 10: retrain and evaluate on human labels | Employer-grouped folds, macro-F1, PR-AUC, keyword-removed ablation. |
| P3 | Rewrite recommender model: implicit-bias rewriting (retrieval, seq2seq or LLM) | Explicit baseline done (Step 10). Step 11 LLM pilot for appearance lines done (5 of 37 distinct texts accepted by checks; 23 rejected). Other implicit units not rewritten. Human evaluation is assigned to the research partner. |
| P4 | External or cross-domain validation | Steps 12 and 8d compare with JABD (English, 2012-2014 EMSCAD). A Philippine or Taglish external corpus was not found; JABD category definitions differ from ours. |
| P5 | Imbalance mitigation comparison for implicit bias | Committee request. Only `class_weight="balanced"` tested so far. |
| P6 | Reproducibility details | Hardware partly logged; psutil was installed after the Step 9 run, so re-check RAM capture. |
| P7 | Decide whether to re-run Step 4b and Step 5 | Still on the older 8,005 units. |
| P8 | Re-read the 102 inclusive units at unit level | Open since the "Female/Male" decision. |
| P9 | Fill the Raza et al. DOI/article number | JABD version resolved: v2.0, Zenodo 10.5281/zenodo.21828061 (concept DOI 10.5281/zenodo.21828060); still update `literature-support-for-methods.md`. |
| P10 | Manuscript text for Step 8 and Step 9 | Claims on collection period, PESO permission and posting dates in 2.1 and 2.2 cannot be verified from the workspace. |
| P11 | Commit the Step 8 and Step 9 notebooks to git | Step 9 notebook is untracked. |

## Open issues found in the Step 9 test

| # | Issue | Evidence |
|---|---|---|
| I1 | Boilerplate line flagged as implicit | "For inquiries and referral, visit or contact:" scored 0.66 with no rule match. |
| I2 | `neutral_statement` has 0 silver units | The model has 3 classes, not 4. |
| I3 | Explicit class has only 50 distinct texts | Its high F1 mostly reflects repeated text. |
