# EduGuard AI

**Student Dropout Early-Warning & Academic Risk Intelligence System** — NTI graduation project.

A multi-page Flask platform for academic advisors: student management, three operational prediction workflows, calibrated dropout risk, local SHAP explanations, actionable recommendations, cohort analytics, and CSV reporting. Student data and prediction histories persist in SQLite.

## Project Overview

EduGuard AI is a bilingual English/Arabic decision-support system that estimates student dropout risk from information available by the end of Semester 1. It helps academic advisors prioritize review and support; it does not make final academic decisions.

## Project Structure

```text
project NTI/
|-- app.py
|-- config.py
|-- requirements.txt
|-- requirements-dev.txt
|-- requirements_ml.txt
|-- README.md
|-- DEPLOYMENT.md
|-- .env.example
|-- .gitignore
|-- render.yaml
|-- gunicorn.conf.py
|-- pytest.ini
|-- services/
|-- repositories/
|-- templates/
|-- static/
|   |-- css/
|   |-- js/
|   |-- img/
|   |-- fonts/
|   `-- vendor/
|-- translations/
|-- tests/
|-- data/
|   |-- raw/data.csv
|   |-- processed/.gitkeep
|   `-- reference/
|       |-- category_labels.json
|       |-- uci_metadata.json
|       `-- final_v2_metrics.json
|-- models/
|   |-- student_dropout_flask_bundle.pkl
|   |-- student_risk_model.pkl
|   |-- probability_calibrator.pkl
|   `-- model_metadata.json
|-- notebooks/
|   `-- NTI_Student_Dropout_FINAL_V2.ipynb
|-- artifacts/
|   |-- enrolled_students_risk_scores.csv
|   `-- feature_dictionary.csv
|-- exports/
|   `-- final_v2/  (isolated validated export; production loads models/)
|-- instance/
|   |-- eduguard.db
|   `-- .session-secret
|-- uploads/.gitkeep
|-- docs/
|   |-- FINAL_PROJECT_AUDIT.md
|   |-- POWERPOINT_SLIDE_REPORT.md
|   |-- FINAL_V2_VALIDATION.md
|   |-- FINAL_AUDIT_HASHES_BEFORE.json
|   `-- FINAL_AUDIT_HASHES_AFTER.json
|-- archive/notebooks/
|   |-- NTI_Student_Dropout_FINAL_COMPLETE.ipynb
|   `-- NTI_Student_Dropout_FINAL_STRONG_CLEAN.ipynb
`-- venv/  (existing environment; kept unchanged)
```

`data/processed/` is reserved; no extra cleaned dataset was invented. Notebook file paths locate the project root whether the notebook is opened from the root or `notebooks/`. Running the notebook's training/export cells is optional and overwrites exported artifacts intentionally; no notebook cells were run during cleanup. The current app stores upload batches in SQLite, not in `uploads/`.

Production from the project root: `gunicorn --config gunicorn.conf.py 'app:create_app()'`. Railway uses this Gunicorn entry point and the existing relative frontend asset URLs. See [deployment preparation](DEPLOYMENT.md) for the SQLite and hosting boundary.

## Installation

Use Python 3.11 and install the pinned dependencies into the project's virtual environment:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

The pinned versions match the environment used to validate the serialized model artifacts. Do not replace the model packages with arbitrary versions.

## Local Run

From the project root in PowerShell:

```powershell
.\venv\Scripts\python.exe app.py
```

Open **http://127.0.0.1:5000**. The application binds to loopback and runs with debug disabled. If it is already running, use the open local URL; stop that server with Ctrl+C before starting another on the same port.

The existing environment already contains all required packages. It was not rebuilt or modified. On a separate installation, use Python 3.11 and install `requirements.txt` into an appropriately managed environment. The versions in that file match the environment used to validate these serialized artifacts; changing scikit-learn/XGBoost versions may make old pickle exports incompatible.

No external API key, database server, CDN, or live network connection is required to run. Chart.js, Lucide icons, and Inter fonts are vendored under `static/`.

## Windows Local Auto Start

The permanent local address is **http://127.0.0.1:5000**. Install the Windows logon task once by running:

```powershell
.\scripts\install_eduguard_startup.bat
```

It creates or updates the **EduGuard AI Local Server** Task Scheduler task, which starts Waitress after you sign in. Start it manually with `.\scripts\start_eduguard.bat`; remove the task with `.\scripts\remove_eduguard_startup.bat`. Confirm readiness at **http://127.0.0.1:5000/health**.

The address stays the same, but localhost is available only while this Windows computer is powered on, you are signed in, and the EduGuard server process is running.

## Local Windows Demo

Use **http://127.0.0.1:5000** for the local demo. It is served by Waitress and can be started manually with `scripts/start_eduguard.bat` or automatically after Windows login with the Task Scheduler installer. The PC must be powered on and the server process must be running.

## Public Demo

The live Railway public demo is **https://eduguard-ai-production-6669.up.railway.app**. It is independent of the laptop and can be reached from phones or other computers. Railway's Trial/free resources are time- and usage-limited; the service may stop when included credits are exhausted, and SQLite data is not a durable production database unless a supported persistent volume is active.

## Problem

Academic difficulties can be discovered too late for timely support. Manual monitoring of large cohorts makes it hard for advisors to identify students who need help early.

## Solution

EduGuard AI consolidates student records and interpretable risk estimates, helping advisors prioritize conversations, tutoring, assessment follow-up, and financial assistance. It supports decisions; it does not make automated decisions about students.

## Dataset

The original `data/raw/data.csv` contains **4,424 students**, **36 input features**, and three source outcomes:

| Outcome | Rows | Operational interpretation |
|---|---:|---|
| Graduate | 2,209 | Resolved negative label: 0 |
| Dropout | 1,421 | Resolved positive label: 1 |
| Enrolled | 794 | Unresolved current students, never relabeled Graduate |

The application uses the **end-of-Semester-1 model**, with **30 exact raw inputs**. Six Semester-2 columns are excluded to prevent future-information leakage. Student IDs and names are application identifiers and never enter the feature DataFrame. `Daytime/evening attendance` is study schedule, not an attendance percentage.

Source: Realinho, Vieira Martins, Machado, and Baptista (2021), [Predict Students' Dropout and Academic Success, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success), [DOI 10.24432/C5MC89](https://doi.org/10.24432/C5MC89), CC BY 4.0. `data/reference/uci_metadata.json` caches the official variable definitions; `data/reference/category_labels.json` extracts readable category labels. Exported bundle course/binary labels and original numerical codes are preserved. Unknown labels remain explicitly labeled source codes, never guessed meanings.

## ML Pipeline

The FINAL V2 notebook prepares resolved Graduate/Dropout outcomes, excludes Semester-2 future variables, validates data quality, applies feature-aware preprocessing, evaluates models with stratified cross-validation, calibrates the selected probability, and evaluates once on an untouched test set. Flask only loads the resulting artifacts; it never retrains them.

## Models Evaluated

The FINAL V2 validation compared Logistic Regression, Random Forest, Extra Trees, and XGBoost. Logistic Regression is the interpretable baseline; the tree ensembles capture non-linear tabular patterns; XGBoost achieved the strongest cross-validated PR-AUC.

## Final Model

The inspected `models/student_dropout_flask_bundle.pkl` contains these actual keys:

```text
model                 sklearn.pipeline.Pipeline
calibrator            sklearn.isotonic.IsotonicRegression
input_features        ordered list of 30 columns
dropout_class_index   1
medium_risk_threshold 0.3
high_risk_threshold   0.4736842215061188
review_margin         0.08
course_map            17 course codes and labels
binary_maps           study schedule and yes/no/gender mappings
```

It is selected because it is the complete operational export. The pipeline has the inspected `preprocessor` and `classifier` steps, with a fitted XGBoost classifier. It expands the 30 raw inputs into 218 transformed features.

The pipeline predicts the Dropout class probability, which then passes through the exported isotonic calibrator. Classification boundaries are:

- Low: probability < 0.30.
- Medium: 0.30 ≤ probability < 0.4736842215061188.
- High: probability ≥ 0.4736842215061188.
- Manual review: absolute distance from the high threshold ≤ 0.08. This is a separate flag, not a fourth risk band.

No fitting or retraining occurs in Flask. Feature order is checked against both the fitted model and exported metadata. If the bundle is absent, the loader supports the inspected split files (`models/student_risk_model.pkl`, `models/probability_calibrator.pkl`, and `models/model_metadata.json`). Missing/incompatible artifacts produce a visible unavailable state instead of fake predictions. Only the existing trusted local artifacts are deserialized; uploaded pickle files are rejected.

## Final Metrics

FINAL V2 selected **XGBoost**. Its executed results were: Accuracy **86.91%**, Precision **78.21%**, Recall **92.25%**, F1 **84.65%**, PR-AUC **93.78%**, ROC-AUC **95.31%**, and Brier score **0.0775**. Cross-validated PR-AUC was **92.77%**; train PR-AUC was **98.66%**, a **5.90 percentage-point** train/CV gap. These submission metrics are documented in `data/reference/final_v2_metrics.json`; they are not recomputed by the Flask application.

Sixteen Enrolled source records contain valid categories absent from the training split. The exported `OneHotEncoder(handle_unknown='ignore')` already handles them. These source-compatible codes are accepted without retraining, and analysis results explicitly note this condition. Out-of-domain codes are rejected.

## Three complete workflows

1. **Existing student:** search/select an ID or real supplied name, load all features, run analysis without a page refresh, view explanations and recommendations, and open the full profile. Each analysis appends history.
2. **Manual entry:** eight steps cover identity, personal information, admission, family/socioeconomic context, finances, Semester 1, economic context, and review. Browser/backend validation reject missing/non-finite values, invalid categories, inappropriate grades, negative/non-integer counts, and approved units greater than enrolled units. “Use sample student” loads one complete actual Enrolled source row. Analysis previews are not automatically persisted; Save Student stores the record and its analysis. Existing IDs cannot be overwritten.
3. **CSV/Excel:** select or drop `.csv`/`.xlsx`, review the first ten rows and validation results, then import and analyze valid rows. Invalid rows are explicitly reported and skipped. The summary includes imported/analyzed counts, risk distribution, failed rows, and a batch CSV download.

Use **Download CSV template** on Upload Data to obtain exact required columns. `Student ID` and `Student Name` are optional. Missing IDs receive deterministic local sequential IDs (`STU-000001`, etc.), checked for collisions. No student names are fabricated. Supplied IDs must contain 1–64 letters, digits, underscores or hyphens. CSV should be UTF-8; common comma, semicolon, and tab delimiters are accepted. The first XLSX worksheet is imported. Formulas are not evaluated; cells without stored numeric values fail required-input validation.

Uploads are limited to 15 MB and 5,000 rows, with an XLSX expansion-size guard. Secure filenames are used. Required/extra/duplicate columns and duplicate IDs are reported. Extra columns—including Semester 2, Target, and old Risk Score—are never used for inference. Raw upload files are processed in memory, not retained on disk. Session-bound preview data is stored temporarily in SQLite and removed on subsequent uploads after 24 hours. Repeated commits return the previous completed result; they cannot duplicate a completed batch. If the application process is terminated during an import, re-upload the file and inspect duplicate-ID validation before retrying.

## Explainable AI

Tree SHAP runs on the fitted XGBoost classifier after preprocessing. Encoded-category contributions are aggregated back to original fields; the top positive and negative contributors are returned. These contributions explain the **underlying model log-odds before calibration**, not percentage-point contributions to the final calibrated probability, causal effects, or confidence intervals.

If SHAP fails, prediction remains available with an explicitly labeled rule-based observed-signal fallback.

## Advisor Recommendation Engine

Recommendations are a separate service and use only actionable academic/financial information: approval rate, grades, missed evaluations, debt, tuition status, and scholarship eligibility when financial issues exist. Gender, nationality, age, parents' education and occupations never determine recommended interventions.

## Flask Features

```text
app.py                         Flask factory, page/API/export routes, error handling
config.py                      Paths, upload limits, local configuration
services/model_service.py      Cached artifact loading, schema, validation, calibration, SHAP
services/recommendation_service.py  Academic/financial snapshots and advisor actions
services/import_service.py     File parsing, preview validation, atomic import commits
services/dashboard_service.py  Analytics derived from actual persisted records
services/presentation_service.py  Read-only FINAL V2 data and bilingual presentation slides
repositories/student_repository.py SQLite transactions, seeding, filtering and history
templates/                     Base shell, pages, shared forms/tables, error page
static/css/app.css             Custom responsive design and reduced-motion behavior
static/js/                     Fetch interactions, charts, search, steppers and imports
static/css/powerpoint.css      Presentation viewer styling and responsive slide layout
static/js/powerpoint.js        Keyboard, touch, fullscreen and Chart.js presentation controls
static/vendor/ and fonts/      Local third-party browser assets
data/                          Cached official category metadata
instance/eduguard.db            Runtime database (not committed)
instance/.session-secret       Generated local session-signing secret (not committed)
tests/test_application.py       Real-artifact integration/regression checks
```

SQLite tables:

- `students`: unique local ID, optional name, course, source, feature JSON, latest probability/risk/review flag, timestamps.
- `analysis_history`: student foreign key, probability, risk/review flags, complete immutable result JSON (including features, factors, recommendations, model stage), timestamp.
- `data_imports`: filename, row count, successful and failed row counts, timestamp.
- `import_batches`: session-owned preview payload, status, and completed result for replay protection.

Student insertion and analysis history commit in the same transaction. WAL mode and short database transactions support normal local interactive use. Timestamps are UTC; profiles show the most recent 100 analyses. All history remains in SQLite.

On first startup with an empty student table, the repository reads complete features directly from `artifacts/enrolled_students_risk_scores.csv`, filters `Target == Enrolled`, and recomputes predictions. No files are joined by row order. The validated current cohort contains **794 records**, **485 High**, **0 Medium**, **309 Low**, and **140 manual-review flags**. Recalculated scores match the supplied risk-score CSV to its published precision. Subsequent starts do not duplicate the seed.

Set `EDUGUARD_SECRET_KEY` to a stable secret if managing configuration externally. Otherwise a random secret is generated once in `instance/`. Session cookies are HttpOnly/SameSite=Lax, write APIs require a CSRF token, exported user text is protected against CSV formula injection, and API/export responses disable caching.

## Routes and APIs

| Page | Route |
|---|---|
| Dashboard | `/`, `/dashboard` |
| Student directory | `/students` |
| Student profile | `/students/<student_id>` |
| Three analysis modes | `/analyze` |
| Upload | `/upload` |
| Model insights | `/model` |
| Dataset and feature dictionary | `/dataset` |
| Reports | `/reports` |
| PowerPoint | `/powerpoint` |
| Health check | `/health` |
| About project | `/about` |

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/dashboard` | Actual cohort analytics |
| GET | `/api/students` | Search/filter/sort/paginate records |
| GET | `/api/students/search?q=` | Debounced selector/global search |
| GET | `/api/students/<id>` | Full record and recent history |
| GET | `/api/sample` | One real source row |
| POST | `/api/analyze/<id>` | Analyze and save an existing student's history |
| POST | `/api/analyze/manual` | Validate and preview manual analysis |
| POST | `/api/students` | Validate, analyze, and save a new manual student |
| POST | `/api/upload` | Multipart `file`; preview and validation |
| POST | `/api/upload/commit` | JSON `token`; import valid rows and analyze |
| GET | `/exports/template.csv` | Empty template with exact model columns |
| GET | `/exports/students.csv` | Filtered current records and model features |
| GET | `/exports/students.csv?risk=High` | High-risk records |
| GET | `/exports/students.csv?batch=<token>` | Session-owned imported batch results |
| GET | `/exports/summary.csv` | Filtered aggregates per risk band |

Student filters include `q`, `risk`, `course`, `review` (0/1), `source`, `min_risk`, `max_risk`, `date` (YYYY-MM-DD), `sort` (risk/id/name/course/date), `direction` (asc/desc), `page`, and `per_page` (maximum 100).

## Bilingual Support

The complete interface supports English LTR and Arabic RTL. The selected language persists through navigation, while presentation labels change without changing model feature names, feature order, numeric codes, thresholds, predictions, or database values.

## Academic PowerPoint

`/powerpoint` is a 20-slide academic graduation-project deck inside Flask. It supports Arabic RTL and English LTR, one-slide navigation, keyboard controls, touch swipe, fullscreen mode, progress, and responsive layouts. Its current slide-by-slide discussion guide is [POWERPOINT_SLIDE_REPORT.md](docs/POWERPOINT_SLIDE_REPORT.md).

## Tests

```powershell
.\venv\Scripts\python.exe -m compileall -q -x 'venv' .
.\venv\Scripts\python.exe -B -m unittest discover -s tests -v
.\venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
```

Compilation deliberately excludes `venv` to honor its preservation requirement. Tests create a temporary database and temporary in-memory CSV/XLSX files; no test students are left in the presentation database. Checks cover actual model loading and feature order, all 794 seed scores, calibration, SHAP and fallback, threshold boundaries, all pages, search/filtering, existing/manual predictions, validation, saving, CSV/XLSX imports, duplicate prevention, missing columns, invalid file types, size limits, batch ownership/replay, exports, CSRF, and formula-injection protection.

Browser checks use isolated headless Chrome, a temporary profile/database and websocket-client. They cover both languages, the cinematic intro, all eight manual steps, uploads and viewport widths from 320 to 2560 pixels. Install `requirements-dev.txt` only in an environment you intend to modify; the cleanup validation used pytest from an OS temporary directory to keep the existing `venv/` untouched. `pytest.ini` limits discovery to `tests/`. Browser checks skip when Chrome or websocket-client is unavailable. Tests may recreate disposable `test-output/`; it is not required by the application.

See [final project audit](docs/FINAL_PROJECT_AUDIT.md), [PowerPoint slide report](docs/POWERPOINT_SLIDE_REPORT.md), and [FINAL V2 validation results](docs/FINAL_V2_VALIDATION.md). The earlier [PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md) is retained as historical cleanup notes.

## Limitations

- This is a complete **graduation-project application**, without authentication, role-based authorization or encryption at rest. Railway/Gunicorn deployment preparation and the SQLite boundary are documented in `DEPLOYMENT.md`. The advisor profile is explicitly a placeholder. Add these controls and appropriate institutional data governance before using real confidential records or exposing it beyond localhost.
- The dataset comes from one higher-education context. Validate/retrain on institutional historical data, monitor calibration and drift, and evaluate fairness across demographic groups before deployment.
- Evaluation metrics are absent from `models/model_metadata.json`; the Model Insights page says “Not available in exported metadata.” No metrics are invented or recomputed on training data.
- Enrollment-stage modeling is discussed in the notebook and educational pages; only the exported Semester-1 model is exposed for operational predictions.
- Bulk analysis is a bounded synchronous operation, with an honest processing indicator. A background job queue and durable recovery would suit larger deployments.
- Exports contain latest student results, not longitudinal history. PDF reporting, authenticated case management, LMS/SIS/ERP connections and opt-in advisor alerts are future extensions.
- Risk is not certainty. A calibrated 100% output is still a model estimate, not an assurance about an individual student's future. Recommendations are advisory and use no sensitive demographic intervention rules.

The original notebook, data CSVs, trained artifacts, metadata, ML requirements, and virtual environment remain in place and unmodified.
