# Draft Discussion: Gender-Bias Detection on PESO Advertisements (Steps 13–14)

Status: draft for review. All values are from `outputs\equal_step13_gender_detector\` and `outputs\equal_step14_transformer_comparison\`. Labels are rule-derived (silver); no human adjudication was done.

## 5.1 Detection and Classification Performance

On the 7,280 in-scope units (691 `unclear` units excluded), a TF-IDF logistic-regression detector separated biased from not-biased units with precision 1.000, recall 0.957 and F1 0.978 (95% CI 0.954–0.995) under employer-grouped five-fold cross-validation. For the three-class task, per-class F1 was 0.999 (none), 0.921 (implicit) and 0.995 (explicit), with a macro-F1 of 0.972 (CI 0.889–0.992) against 0.325 for a majority-class baseline. Span localisation reached an F1 of 0.997 when the biased unit was given and 0.977 end to end.

These figures should be read as a measure of how faithfully the models reproduce the annotation rules, not as accuracy against human judgement. The labels were produced by a deterministic pre-annotator (Layer A/B schema), so any model that learns the same lexical cues will score highly. Three observations support this reading. First, when the label-defining words were removed from the text, TF-IDF macro-F1 fell from 0.972 to 0.542 and implicit F1 from 0.921 to 0.107. Second, the explicit class contains 313 units but only 12 distinct texts, and the implicit class 38 units (24 distinct texts), so near-duplicate advertisement boilerplate dominates the minority classes. Restricting the evaluation to distinct texts did not change the picture (macro-F1 0.978 on 4,288 units), which shows that duplication alone does not explain the scores, but the small number of distinct explicit and implicit examples keeps the estimates fragile. Third, the implicit F1 interval is wide (0.667–0.982).

The implicit class here consists only of gendered titles and pronouns (e.g., "salesman", "foreman"). Under the adopted schema, agentic/communal wording is not treated as bias by default, because such terms can describe legitimate duties; these 577 units were routed to manual review and no stereotyping labels exist. The study therefore does not yet evaluate detection of stereotype-based implicit bias, and the term "implicit" should not be read as covering it.

## 5.2 Context-Aware Models Did Not Improve on Keyword-Based Features

Fine-tuned BERT-base and RoBERTa-base were compared with TF-IDF on identical folds and bootstrap resamples. BERT reached a macro-F1 of 0.957 (0.898–0.988); the paired difference from TF-IDF was −0.015 (95% CI −0.059 to 0.031), so no difference can be claimed. RoBERTa reached 0.728 (0.601–0.831), a paired difference of −0.244 (−0.369 to −0.140), with 132 out-of-fold errors against 9 for TF-IDF and 10 for BERT. Its errors were mostly explicit units labelled none (58) or implicit (35), and none units labelled explicit (18).

With the label-defining words removed, none of the models retained the signal: macro-F1 was 0.542 for TF-IDF, 0.354 for BERT (paired difference −0.188, −0.226 to −0.143) and 0.399 for RoBERTa (−0.143, −0.196 to −0.085). RoBERTa's biased-vs-not F1 in this setting (0.997) came with predictions that were almost entirely the implicit class, and we attribute it to residue left by the word-stripping step rather than to contextual understanding; we do not report it as evidence of context-sensitivity.

These results do not support the hypothesis that a context-aware encoder improves precision over keyword-based features for explicit bias on this dataset. They also do not show that such models are worse at detecting bias in general. Because the labels are lexical, there is little contextual information for a transformer to add, and an accurate comparison requires labels that were not derived from the same word lists. The transformers were trained with a fixed configuration (three epochs, learning rate 3e-5, `none` capped at 1,500 distinct training texts) and no tuning on a CPU; the weaker RoBERTa result may reflect under-training and should not be generalised.

## 5.3 External Evidence from JABD

The same families of rules were checked against the human-annotated Job Ad Bias Dataset (JABD v2.0), restricted to gender. The Layer B rules (with unclear units flagged) reached a precision of 0.825, recall of 0.506 and F1 of 0.627 for gendered-bias sentences, compared with 0.814, 0.466 and 0.593 for the earlier rules. The strict Layer B explicit class had a precision of 0.857 but a recall of 0.007. Of JABD's 1,685 explicit-gender sentences, 508 contained no gender word, so lexical rules cannot reach them. JABD's labels are broader than ours (for example, generic pronouns and equal-opportunity statements), and the corpus is enriched for biased language by a lexicon, so these figures reflect a difference in definition as much as in performance. They show that the rules have high precision and limited recall on an independent, human-annotated source.

## 5.4 Annotation Design as a Contribution

Separating gender reference (Layer A), bias judgement and rewrite decision (Layer B) changed the labels materially. Of the 484 units previously labelled explicit, 313 remained explicit, 110 became unclear and 61 became none (mostly age and civil-status lines, which fall outside the gender scope). Of 668 units previously labelled implicit, 579 became unclear, 88 none and 1 implicit. The schema also keeps binary listings such as "Female/Male" as a gender reference with a recommended rewrite instead of a discriminatory label. The detector nevertheless labelled 101 of 106 such units explicit, because it was never trained on that class; this shows that the classifier does not yet implement the schema's distinction and that the unclear category needs human adjudication.

## 5.5 Limitations

1. All PESO labels are rule-derived silver labels; no human adjudication or inter-annotator agreement is available. Reported scores measure reproduction of the rules.
2. The explicit class has 12 distinct texts and the implicit class 24, so the results are sensitive to a small number of examples.
3. Span gold labels come from the same rules, so the span scores are an upper bound; exact, overlap and token metrics coincide because the spans are single words.
4. The final model missed "Must be male, 25-30 years old" in a demonstration, indicating limited handling of restrictions embedded in longer sentences.
5. The transformer comparison used one fixed configuration, no hyperparameter search, CPU training and a capped negative class. It covers classification only, not spans.
6. Earlier pipeline steps (silver classifier, rule-based and LLM rewrites) use the previous explicit definition, which included age and civil status, and were not regenerated under the Layer A/B schema.
7. JABD (2012–2014 postings, lemmatised text, lexicon-enriched) differs in period, language variety and definition from PESO advertisements.

## 5.6 Implications and Future Work

The classifier is suitable as a screening and pre-annotation tool that proposes labels and spans for human review, and its evaluation should be completed with human-labelled data and agreement statistics. Transformer comparisons should be repeated once labels are independent of the word lists, since only then can a contextual advantage, if any, be measured. Extending the schema to evaluate coded wording in context is the main step needed to evaluate implicit bias beyond gendered titles.
