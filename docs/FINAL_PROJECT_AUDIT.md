# EduGuard AI Final Project Audit

Audit date: 2026-09-16  
Scope: final repository cleanup, production-safety verification, and graduation-project documentation.

## 1. Project Overview

EduGuard AI is a bilingual Flask decision-support platform for early identification of student academic dropout risk. It combines an end-of-Semester-1 machine-learning workflow with calibrated risk probabilities, global and local explanations, advisor recommendations, dashboards, manual entry, existing-student analysis, CSV/Excel import, reports, and an interactive 20-slide academic presentation.

The system estimates risk for review and support. It does not make an automatic academic decision, prove causation, expel a student, or describe a probability as certainty.

## 2. Final Architecture

data/raw/data.csv  
→ notebooks/NTI_Student_Dropout_FINAL_V2.ipynb  
→ models/ (live Flask artifacts) and exports/final_v2/ (isolated validated export)  
→ services/model_service.py and services/recommendation_service.py  
→ repositories/student_repository.py and instance/eduguard.db  
→ Flask routes/APIs in app.py  
→ templates, static, translations  
→ Dashboard, Students, Analyze, Upload, Model, Dataset, Reports, About, PowerPoint

Flask loads the trusted bundle under models/ first and supports the inspected split-artifact fallback. No fitting or retraining occurs in Flask.

## 3. ML Pipeline

The source contains 4,424 rows, 36 original input features, and three outcomes: Graduate 2,209, Dropout 1,421, and Enrolled 794. FINAL V2 reports zero missing values and zero duplicates before drop. Graduate and Dropout become the resolved binary training population (0 and 1); Enrolled remains an unresolved scoring cohort.

The prediction point is the end of Semester 1. Six Semester-2 columns are excluded to prevent future-data leakage: credited, enrolled, evaluations, approved, grade, and without evaluations. The exported operational model uses 30 exact Semester-1-compatible raw inputs in the recorded order. Student ID and Student Name are application identifiers and are excluded from model inputs.

Numeric and categorical typing is preserved in the exported pipeline. Numeric missing values use median imputation, categorical missing values use most-frequent imputation, and categorical variables are one-hot encoded. Impossible values are validated as missing/invalid; valid extreme observations are retained. RobustScaler is used for Logistic Regression only. Tree models use the original numeric scale because their split decisions do not require scaling.

The resolved population is split into train, calibration, and untouched test partitions of 2,323, 581, and 726 rows. Candidate models are Logistic Regression, Random Forest, Extra Trees, and XGBoost. Five-fold Stratified Cross-Validation preserves class proportions. PR-AUC is the primary selection metric because Dropout is the positive class under imbalance. Class weighting is used for supported models and scale_pos_weight for XGBoost; SMOTE was not used because weighting was sufficient and avoids synthetic student records.

The selected XGBoost is calibrated with Isotonic Regression. The exported high threshold is 0.48148149251937866, medium threshold is 0.3, and human-review margin is 0.08. Threshold tuning targeted a minimum Recall of 85%.

## 4. Models

| Model | Role | CV PR-AUC |
|---|---|---:|
| Logistic Regression | Interpretable baseline; RobustScaler | 0.9238844665 |
| Random Forest | Nonlinear bagged tree ensemble | 0.9182875735 |
| Extra Trees | High-randomness comparison | 0.8959963732 |
| XGBoost | Gradient boosting; selected | 0.9276638343 |

XGBoost was selected because it achieved the strongest cross-validated PR-AUC in this executed comparison. This is not a universal claim.

## 5. Final Metrics

All values below are read from data/reference/final_v2_metrics.json.

| Measure | Executed value |
|---|---:|
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
| Review margin | 0.08 |
| Enrolled total | 794 |
| Enrolled Low | 309 |
| Enrolled Medium | 0 |
| Enrolled High | 485 |
| Enrolled Human Review | 140 |

The Train-to-CV difference is a moderate gap of approximately 5.90 percentage points. Validation and untouched-test performance remain strong; the gap must not be described as negligible.

## 6. Explainability

Permutation importance measures the performance change when a feature is shuffled. SHAP attributes model-output contribution for an individual or global summary. Flask computes Tree SHAP for individual predictions and labels contributions as associations, not causes or percentage-point changes.

Leading stored examples include Curricular units 1st sem (approved), Tuition fees up to date, Curricular units 1st sem (grade), Course, and Curricular units 1st sem (enrolled). These rankings describe model behavior and do not prove causation.

## 7. Risk Logic

The calibrated probability is presented as Estimated Dropout Risk. Low is below the medium threshold, Medium is from the medium threshold up to the high threshold, and High is at or above the high threshold. Human Review is a separate flag when probability is within the exported margin around the high threshold. It can overlap a risk band.

For the current FINAL V2 Enrolled cohort: Low 309, Medium 0, High 485, Human Review 140. The Medium band exists; no current student falls inside it in this cohort. That is a cohort result, not a system error.

## 8. Advisor Recommendation Engine

services/recommendation_service.py uses transparent rules over actionable Semester-1 academic and financial signals. It can recommend advisor meetings and tutoring for low approval, a study plan for a low Semester-1 grade, missed-assessment review for units without evaluations, and financial support/payment-plan/scholarship review for tuition or debtor signals. Recommendations are advisory and do not use sensitive characteristics as intervention reasons.

## 9. Flask Features

- / and /dashboard: cohort KPIs, risk distribution, course chart, high-risk list, and threshold/review explanations.
- /students: searchable, filterable, sortable, paginated directory.
- /students/<student_id>: snapshots, factors, recommendations, features, and history.
- /analyze: existing-student, manual eight-step, and analysis workflows.
- /upload: CSV/Excel preview, validation, import, analysis, and download.
- /model: model insights.
- /dataset: dataset explanation and grouped feature dictionary.
- /reports: filtered results and CSV exports.
- /about: project story and decision-support boundary.
- /powerpoint: bilingual, one-slide-at-a-time, 20-slide viewer.

## 10. Bilingual System

The centralized translation catalog and language state are shared by Flask templates and JavaScript. English uses lang=en dir=ltr; Arabic uses lang=ar dir=rtl. The same feature names, codes, feature order, thresholds, predictions, and database values remain unchanged. Bundled Noto Sans Arabic supports readable Arabic UI. PowerPoint has parallel English/Arabic slide catalogs.

## 11. PowerPoint System

The viewer contains exactly 20 academic slides covering title, idea, problem, objectives, scope, dataset, target preparation, leakage, preprocessing, outliers, imbalance, models, cross-validation, calibration, final results, evaluation, explainability, current-student scoring, recommendations, and the complete system/conclusion. It supports Previous/Next, arrow keys, Space, fullscreen, progress, slide count, touch swipe, Chart.js charts, reduced-motion-aware transitions, and RTL. The actual slide report is docs/POWERPOINT_SLIDE_REPORT.md and the machine-readable report is data/reference/powerpoint_slide_report.json.

## 12. Deployment

Development: .\venv\Scripts\python.exe app.py  
Production: gunicorn --config gunicorn.conf.py 'app:create_app()'

render.yaml, gunicorn.conf.py, .env.example, requirements.txt, and DEPLOYMENT.md remain. Local SQLite remains supported. A public multi-user deployment should use persistent PostgreSQL or equivalent managed storage. No credentials were added.

## 13. Tests

The full suite completed with 68 passed, 4 warnings, and 256 subtests passed. Browser checks cover English/Arabic, RTL, the PowerPoint viewer, 20 active-slide count, controls, geometry, responsive widths, and no document overflow. Three warnings are third-party SHAP deprecations and one is a Python invalid-escape warning in an existing test docstring; no test failed.

## 14. Final Folder Structure

project NTI/
├── app.py, config.py, requirements*.txt, README.md
├── DEPLOYMENT.md, render.yaml, gunicorn.conf.py, .env.example, .gitignore
├── services/, repositories/, templates/, static/, translations/, tests/
├── data/raw/data.csv
├── data/processed/.gitkeep
├── data/reference/
├── models/
├── artifacts/
├── exports/final_v2/
├── notebooks/NTI_Student_Dropout_FINAL_V2.ipynb
├── archive/notebooks/
├── instance/
├── uploads/.gitkeep
└── docs/

## 15. Cleanup Performed

- Inspected source, templates, static assets, translations, tests, data, models, notebooks, deployment files, exports, database, and generated output.
- Recorded before/after critical hashes in docs/FINAL_AUDIT_HASHES_BEFORE.json and docs/FINAL_AUDIT_HASHES_AFTER.json.
- Deleted only generated caches, browser/test output, bytecode, logs, and the unreferenced duplicate artifacts/requirements_ml.txt.
- Archived two historical notebooks instead of deleting them.
- Preserved models, data/raw, the enrolled risk-score CSV, the database, the final V2 notebook, and live presentation files.
- Updated README structure and cleanup links; no runtime path was changed.

### File-audit classification

| Classification | Current groups | Decision |
|---|---|---|
| REQUIRED | app.py, config.py, services, repositories, templates, static, translations, models, data/raw, data/reference, artifacts, instance, uploads/.gitkeep, requirements, deployment files | Kept and verified by imports, route references, tests, or documented runtime paths. |
| DEVELOPMENT ONLY | tests, requirements-dev.txt, venv | Kept; venv was not modified. |
| DOCUMENTATION | README.md, DEPLOYMENT.md, docs, vendor/font licenses | Kept; final audit and slide reports were added. |
| ARCHIVE CANDIDATE | Two superseded notebooks | Moved to archive/notebooks for historical value. |
| SAFE TO DELETE | __pycache__, .pytest_cache, test-output, logs, browser screenshots, duplicate artifacts/requirements_ml.txt | Deleted after reference checks. |
| UNKNOWN | None identified | No ambiguous source, model, data, route, or deployment file was deleted. |

## 16. Files Deleted

72 files were removed: the historical generated/cache inventory (54 files), 11 newer screenshots/logs, five pytest-cache files, the unreferenced duplicate artifacts/requirements_ml.txt, and the temporary report generator. No source, model, dataset, database, route, or required static asset was deleted.

## 17. Files Archived

archive/notebooks/NTI_Student_Dropout_FINAL_COMPLETE.ipynb  
archive/notebooks/NTI_Student_Dropout_FINAL_STRONG_CLEAN.ipynb

Their contents were not modified and Flask does not load them.

## 18. Files Moved

Two historical notebook files moved from notebooks/ to archive/notebooks/. No runtime file moved.

## 19. Paths Updated

Only README documentation paths were updated for the archive, exports/final_v2, and final reports. Model loading, database paths, routes, templates, static URLs, and the FINAL V2 notebook path were unchanged.

## 20. Dead Code Removed

No production Python, template, CSS, or JavaScript code was removed during this final cleanup. Only generated bytecode/output and the unreferenced duplicate ML requirements file were removed.

## 21. Production Artifacts Verification

All critical SHA256 values match the pre-cleanup snapshot. The live bundle, split model, calibrator, metadata, raw dataset, enrolled risk-score CSV, SQLite database, final V2 notebook, presentation service/template/CSS/JS are byte-for-byte unchanged. The before and after records are linked in docs/FINAL_AUDIT_HASHES_BEFORE.json and docs/FINAL_AUDIT_HASHES_AFTER.json.

This confirms ML predictions, thresholds, feature order, calibration, SHAP behavior, database content, bilingual behavior, and PowerPoint content were not changed by cleanup.

## 22. Known Limitations

- The project folder is not a Git working tree, so git status and git diff could not produce repository history; this is recorded in the before snapshot.
- Local SQLite is appropriate for the demo/local workflow; public multi-user deployment needs persistent PostgreSQL or managed storage.
- Authentication, role-based authorization, encryption at rest, institutional governance, and live SIS/LMS integration are not included.
- The dataset comes from one higher-education context; institutional validation, calibration monitoring, drift monitoring, and fairness review are required before real deployment.
- Three third-party SHAP PendingDeprecationWarnings appear during tests; they do not affect results.

## 23. Submission Readiness

The repository is submission-ready for the current graduation-project scope: working Flask routes and bilingual UI are preserved, production model/data/database hashes match the safety snapshot, FINAL V2 evidence is documented, the current PowerPoint is documented slide by slide, generated junk is removed, historical notebooks are retained in an archive, and the full test suite passes. Public deployment still requires a hosting decision, persistent production database, authentication/data governance, and institution-specific validation.
