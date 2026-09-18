# FINAL V2 validation

The final V2 notebook was executed completely in an isolated temporary workspace on the current `data/raw/data.csv`. All 21 original code cells completed with zero errors. The current dataset was staged under the notebook's legacy filename only for that run; the production project files were not written.

## Executed results

| Measure | FINAL V2 result |
| --- | ---: |
| Selected model | XGBoost |
| Train PR-AUC | 0.9866443336008119 |
| CV PR-AUC | 0.9276638343041993 |
| Train/CV gap | 0.05898049929661264 |
| Accuracy | 0.8691460055096418 |
| Precision | 0.7820895522388059 |
| Recall | 0.9225352112676056 |
| F1 | 0.8465266558966075 |
| PR-AUC | 0.9377955609524928 |
| ROC-AUC | 0.9531180294436301 |
| Brier Score | 0.07753758132457733 |
| High-risk threshold | 0.48148149251937866 |
| Medium-risk threshold | 0.3 |
| Enrolled: Low | 309 |
| Enrolled: Medium | 0 |
| Enrolled: High | 485 |
| Enrolled: Human Review | 140 |
| Total Enrolled | 794 |

The final test confusion matrix was `[[369, 73], [22, 262]]`. The run also produced actual ROC, precision–recall and calibration points, bootstrap confidence intervals, permutation importance, SHAP summaries and fairness subgroup measurements. The complete evidence is stored in [final_v2_metrics.json](../data/reference/final_v2_metrics.json).

## Comparison with the current Flask artifacts

The V2 export under `exports/final_v2/` and the live bundle under `models/` match in model metadata and serialized artifact hashes. Both load an XGBoost classifier with the same 30 exact Semester-1 inputs in the same order. Both use the same preprocessing pipeline, the fitted isotonic probability calibrator, the same medium threshold (`0.3`), high-risk threshold (`0.48148149251937866`), and human-review margin (`0.08`). Six Semester-2 fields remain excluded.

Scoring all 794 Enrolled source rows produced an exact match: maximum calibrated-probability difference `0.0`, identical risk levels, identical threshold logic, and identical counts (Low 309, Medium 0, High 485, Human Review 140). Student identifiers and database records were not used as model inputs and were unchanged.

## Promotion decision

**B) Remain submission-only.** FINAL V2 is validated and reproducible, but it is already byte-equivalent to the current Flask production artifacts. There is no evidence-based model change to promote. The application continues to load the existing `models/` files; the notebook's isolated export remains available for review under `exports/final_v2/`.

The notebook load cell has also been made portable to the cleaned project layout by accepting `data/raw/data.csv`; this does not change the dataset, model, thresholds or exported production files.
