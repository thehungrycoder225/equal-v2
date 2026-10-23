# Project tasks

Last updated: 2026-10-23. Status is based on files in this repository. Pending items need your approval before work starts.

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
| 13 | Step 8c Layer B definition and design test (rule pre-annotation, JABD gender-only check); no human labels | `equal-step8c-layerB-test.ipynb` |
| 12 | Step 8b gender-focused Layer A annotation schema and validator (labels empty; Layer B pending) | `equal-step8b-gender-schema.ipynb` |
| 11 | Step 12 external validation on JABD (human-annotated) in place of PESO human labels; label-definition mismatch found | `equal-step12-jabd-validation.ipynb`; data in `external\jabd\` |

## Pending (not started, awaiting approval)

| # | Task | Notes |
|---|---|---|
| P1 | Human-label the 596-unit Step 8 sample | Deferred for time. Partly replaced by Step 12 (JABD external validation), which does not validate the PESO silver labels. |
| P2 | Step 10: retrain and evaluate on human labels | Employer-grouped folds, macro-F1, PR-AUC, keyword-removed ablation. |
| P3 | Rewrite recommender model: implicit-bias rewriting (retrieval, seq2seq or LLM) | Explicit baseline done (Step 10). Step 11 LLM pilot for appearance lines done (5 of 37 distinct texts accepted by checks; 23 rejected). Other implicit units not rewritten. Human evaluation is assigned to the research partner. |
| P4 | External or cross-domain validation | Step 12 done on JABD (English, 2012-2014 EMSCAD). A Philippine or Taglish external corpus was not found. |
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
