# Submission cleanup audit

The entire project was inventoried recursively, including the existing virtual environment (read-only). Application code, templates, styles, scripts, tests, documentation, deployment files and notebook source were searched before any move or deletion.

| Files/group | Classification | Decision and reference evidence |
| --- | --- | --- |
| Application Python, templates, translations, static assets | USED | Route handlers, template includes, CSS imports and script references; kept. |
| Bundled model | USED | `ModelService` primary loader; moved intact to `models/`. |
| Split model and calibrator | USED | Explicit fallback loader; retained despite overlapping purpose with bundle. |
| Model metadata | USED | Loader and feature-order checks; moved intact to `models/`. |
| Original dataset | USED | Model service source data and notebook input; moved intact to `data/raw/`. |
| Enrolled risk scores | USED | Repository seed and regression tests; moved intact to `artifacts/`. |
| Feature dictionary | USED | Dataset page and model service; moved intact to `artifacts/`. |
| Category labels | USED | Model display/schema mapping; moved intact to `data/reference/`. |
| UCI metadata | USED (reference documentation) | README source provenance and cached variable definitions; retained in `data/reference/`. |
| Final notebook | USED | Only notebook found; moved to `notebooks/`, with input/output path adjustments only. Stored results were retained; no cells executed. |
| `requirements_ml.txt` | USED | Notebook export of ML dependency names; distinct from pinned application requirements; retained at root. |
| Render/Gunicorn/environment/deployment files | USED | Current production start and configuration documentation; retained. |
| Font/vendor licenses and vendor README | USED | Attribution for bundled browser assets; retained even where not imported at runtime. |
| Package `__init__.py` files | DUPLICATE bytes, USED | Both empty but establish separate Python packages; retained. |
| `instance/eduguard.db`, `.session-secret` | USED | Runtime records/session state; kept in place, unchanged and ignored for privacy. |
| `venv/` | USED | Existing environment; no files installed, removed, compiled or relocated inside it. |
| 40 existing files under `test-output/` | TEMPORARY / SAFE TO REMOVE | Generated screenshots, logs, browser samples and audits; no individual basename referenced by source/notebook/docs. Browser tests write fresh outputs rather than reading these as fixtures. Removed after checks. |
| Project `__pycache__/` and `.pyc` outside `venv/` | TEMPORARY / SAFE TO REMOVE | Interpreter outputs, no source references; removed after validation. |
| Legacy/experimental notebooks or deployment files | LEGACY | The earlier `FINAL_COMPLETE` and `FINAL_STRONG_CLEAN` notebooks were retained and moved to `archive/notebooks/`; the current submission notebook is `notebooks/NTI_Student_Dropout_FINAL_V2.ipynb`. |

No source/data/model duplicates were deleted. No temporary upload files were present; imports use database-held batches. `uploads/.gitkeep` reserves the requested directory without changing upload behavior. `data/processed/` is reserved and empty: the supplied risk-score CSV is an application artifact, not a separate cleaned dataset.

Dead code removed: unused `re` import in the model service; unused `json`, `loaded_model`, and `ValidationError` imports in application tests; unused `seen` set in import preview. JavaScript state variables were retained where read by validation/reset handlers. Notebook progress prints are intentional analysis output, not application debugging.

Pytest was provisioned in an OS temporary directory outside the project because it was absent from the protected virtual environment. Compilation excludes `venv/` to honor the explicit no-modification requirement. Generated validation files and bytecode are removed after testing; the durable result is recorded in `VALIDATION.md`.

## Removed pre-existing generated files

- `repositories/__pycache__/student_repository.cpython-311.pyc`
- `repositories/__pycache__/__init__.cpython-311.pyc`
- `services/__pycache__/dashboard_service.cpython-311.pyc`
- `services/__pycache__/i18n_service.cpython-311.pyc`
- `services/__pycache__/import_service.cpython-311.pyc`
- `services/__pycache__/model_service.cpython-311.pyc`
- `services/__pycache__/recommendation_service.cpython-311.pyc`
- `services/__pycache__/__init__.cpython-311.pyc`
- `test-output/arabic-about-text.json`
- `test-output/arabic-analyze-text.json`
- `test-output/arabic-dashboard-text.json`
- `test-output/arabic-dashboard.png`
- `test-output/arabic-dataset-text.json`
- `test-output/arabic-dataset.png`
- `test-output/arabic-feature-table.png`
- `test-output/arabic-manual-result-text.json`
- `test-output/arabic-manual-review.png`
- `test-output/arabic-mobile-dataset-320.png`
- `test-output/arabic-mobile-dataset-390.png`
- `test-output/arabic-mobile-navigation.png`
- `test-output/arabic-model-text.json`
- `test-output/arabic-prediction-result.png`
- `test-output/arabic-prediction-stages.png`
- `test-output/arabic-reports-text.json`
- `test-output/arabic-review-values.png`
- `test-output/arabic-students-STU-000001-text.json`
- `test-output/arabic-students-text.json`
- `test-output/arabic-upload-result-text.json`
- `test-output/arabic-upload-text.json`
- `test-output/bilingual-all-tests.log`
- `test-output/bilingual-browser.log`
- `test-output/bilingual-tests.log`
- `test-output/browser-sample.csv`
- `test-output/english-dashboard.png`
- `test-output/i18n-residual.json`
- `test-output/intro-ar-1440.png`
- `test-output/intro-ar-390.png`
- `test-output/intro-en-1440.png`
- `test-output/intro-en-390.png`
- `test-output/release-tests-final.log`
- `test-output/release-tests.log`
- `test-output/responsive-ar-1440.png`
- `test-output/responsive-ar-390.png`
- `test-output/responsive-ar-768.png`
- `test-output/responsive-en-1440.png`
- `test-output/responsive-en-390.png`
- `test-output/responsive-en-768.png`
- `test-output/ui-schema.json`
- `tests/__pycache__/test_application.cpython-311.pyc`
- `tests/__pycache__/test_i18n.cpython-311.pyc`
- `tests/__pycache__/test_i18n_browser.cpython-311.pyc`
- `tests/__pycache__/test_release.cpython-311.pyc`
- `__pycache__/app.cpython-311.pyc`
- `__pycache__/config.cpython-311.pyc`
