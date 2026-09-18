# EduGuard AI deployment

The active public demo is hosted on Railway at **https://eduguard-ai-production-6669.up.railway.app**. The local Windows demo remains `http://127.0.0.1:5000` and uses Waitress. No database migration is performed by either deployment.

## Railway service

The Railway service is connected to the `main` branch and runs the existing Flask factory with Gunicorn:

Build: `pip install -r requirements.txt`

Start: `gunicorn --config gunicorn.conf.py 'app:create_app()'`

Railway supplies `PORT`; `gunicorn.conf.py` binds to `0.0.0.0:$PORT`. Configure `EDUGUARD_ENV=production`, a generated `SECRET_KEY`, `EDUGUARD_DATABASE_PATH`, and `EDUGUARD_SEED_DATABASE` in Railway variables. Include `models/`, `data/raw/`, `data/reference/`, and `artifacts/` with their original trusted files. The factory resolves these directories from the project root using pathlib; no working-directory or Windows-specific model paths are required. Never load untrusted pickle files. Do not upload the local virtual environment, local database, `.env` or `.session-secret`.

Railway terminates HTTPS. Production sets secure, HttpOnly, SameSite session cookies, disables debug/exception propagation and adds HSTS. Frontend assets and API requests use relative URLs. Upload validation, sanitized filenames, CSRF, the 15 MB request limit and 5,000-row limit remain unchanged. `.env.example` is documentation, not an automatically loaded secrets file.

The Railway Trial/free service is suitable for a demonstration, not durable multi-user production. Its filesystem is ephemeral unless a supported volume is attached, and Trial/free credits and volume retention are limited by the hosting plan. The public URL may have a cold start or become unavailable after included usage is exhausted. The local workstation database is never uploaded or replaced.

## Historical Render configuration

`render.yaml` is retained as a historical, no-secret Render Blueprint. It is not the active public deployment. It may be used only for a separately reviewed Render demo; it does not change the Railway service.

Build: `pip install -r requirements.txt`

Start: `gunicorn --config gunicorn.conf.py 'app:create_app()'`

The application exposes a factory, not a module-level `app`. Gunicorn runs on Linux; use the existing Flask development command on Windows. The runtime version is pinned to Python 3.11 to match the exported model environment. Verify dependency availability and model loading in the first Linux build; this workspace's Windows virtual environment is not modified by deployment preparation.

## Persistent storage and database boundary

**LOCAL DEMO: SQLite.** **PUBLIC MULTI-USER DEPLOYMENT: PostgreSQL recommended.**

Only writes beneath an explicitly configured persistent mount survive host restarts. Keep one service instance; SQLite and its WAL files must remain on the same disk. Configure tested backups using SQLite's online backup API or a stopped service; do not copy only a live `.db` file while omitting its WAL. Restore-test backups before public use. Set `EDUGUARD_SEED_DATABASE=false` only when a separately provisioned database is intentionally available.

`EDUGUARD_DATABASE_PATH` is the explicit storage boundary. `StudentRepository` remains the SQLite adapter, shared by imports and dashboard services. PostgreSQL is **not implemented**: `DATABASE_URL` fails fast rather than silently ignoring it or writing to SQLite. A later adapter must preserve repository operations, identifiers, transaction/idempotency semantics and history. Raw SQL also exists in dashboard/report/export handlers and must be ported with the repository; merely changing a URL will not work. Make that a separately reviewed migration with backups and parity tests. Prediction code requires no database dependency changes.

## Public release gate

The current application is an unauthenticated shared workspace: anyone with access can view, import, save and analyze its records. Use only non-sensitive demonstration data for a public demo. A real multi-user student service still needs access control, tenant/role rules and an audited PostgreSQL migration; those would change existing behavior and are intentionally outside this task. No claim of production privacy or multi-tenant isolation is made.

Before creating another service: connect the Git provider, provision the trusted artifacts, and review the initial Linux build and memory usage. Benchmark actual imports and adjust resources/timeouts without changing the model. Custom domain setup is optional; Railway supplies an HTTPS service URL.

References: [Railway Python deployment](https://docs.railway.com/builds/railpack), [Railway public domains](https://docs.railway.com/networking/domains/working-with-domains), [Flask factory with Gunicorn](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/), [Render Flask deployment](https://render.com/docs/deploy-flask).
