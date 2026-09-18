# EduGuard AI deployment

No deployment or database migration has been performed. Development remains `python app.py`.

## Render service

Import this repository as a Render Blueprint using `render.yaml`. The current Blueprint is deliberately configured for Render's **Free web-service plan**: it has no persistent disk and stores the demo SQLite database at `/tmp/eduguard.db`. Include `models/`, `data/raw/`, `data/reference/`, and `artifacts/` with their original trusted files in the repository or provision them securely before startup. The factory resolves these directories from the project root using pathlib; no working-directory or Windows-specific model paths are required. Never load untrusted pickle files. Do not upload the local virtual environment, local database, `.env` or `.session-secret`.

Build: `pip install -r requirements.txt`

Start: `gunicorn --config gunicorn.conf.py 'app:create_app()'`

The application exposes a factory, not a module-level `app`. Gunicorn runs on Linux; use the existing Flask development command on Windows. The runtime version is pinned to Python 3.11 to match the exported model environment. Verify dependency availability and model loading in the first Linux build; this workspace's Windows virtual environment is not modified by deployment preparation.

Render terminates HTTPS. Production sets secure, HttpOnly, SameSite session cookies, disables debug/exception propagation and adds HSTS. Frontend assets and API requests use relative URLs. Upload validation, sanitized filenames, CSRF, the 15 MB request limit and 5,000-row limit remain unchanged. Set `SECRET_KEY` in the service environment (the Blueprint generates one). `.env.example` is documentation, not an automatically loaded secrets file.

## Persistent storage and database boundary

**LOCAL DEMO: SQLite.** **PUBLIC MULTI-USER DEPLOYMENT: PostgreSQL recommended.**

The supplied Blueprint prepares a single-instance SQLite demo with a paid persistent disk mounted at `/var/data`. Only writes beneath that mount persist. An ephemeral filesystem or free service is unsuitable for preserving SQLite student records. The disk is available at runtime, not during the build. Keep one service instance; SQLite and its WAL files must remain on the same disk. Configure tested backups using SQLite's online backup API or a stopped service; do not copy only a live `.db` file while omitting its WAL. Restore-test backups before public use.

On the Free plan, the service starts from the source-data seed and local SQLite writes are temporary. Render can discard `/tmp/eduguard.db` whenever the service redeploys, restarts, or spins down. The local workstation database is never uploaded or replaced. Set `EDUGUARD_SEED_DATABASE=false` only when a separately provisioned database is intentionally available.

Render's Free web services are suitable for a public demonstration, not durable multi-user production: they sleep after inactivity, may take about a minute to wake, and have an ephemeral filesystem. A paid service with a persistent disk or an approved PostgreSQL adapter would be required for durable hosted records; neither is activated by this project.

`EDUGUARD_DATABASE_PATH` is the explicit storage boundary. `StudentRepository` remains the SQLite adapter, shared by imports and dashboard services. PostgreSQL is **not implemented**: `DATABASE_URL` fails fast rather than silently ignoring it or writing to SQLite. A later adapter must preserve repository operations, identifiers, transaction/idempotency semantics and history. Raw SQL also exists in dashboard/report/export handlers and must be ported with the repository; merely changing a URL will not work. Make that a separately reviewed migration with backups and parity tests. Prediction code requires no database dependency changes.

## Public release gate

The current application is an unauthenticated shared workspace: anyone with access can view, import, save and analyze its records. Use only non-sensitive demonstration data for a public demo. A real multi-user student service still needs access control, tenant/role rules and an audited PostgreSQL migration; those would change existing behavior and are intentionally outside this task. No claim of production privacy or multi-tenant isolation is made.

Before creating the service: connect your Git provider to your Render account, approve the service/disk plan, provision the trusted artifacts, and review the initial Linux build and memory usage. The default standard plan is a starting point, not a measured capacity guarantee. Benchmark actual imports and adjust resources/timeouts without changing the model. Custom domain setup is optional; Render supplies an HTTPS service URL.

References: [Render Flask deployment](https://render.com/docs/deploy-flask), [persistent disks](https://render.com/docs/disks), [Python runtime](https://render.com/docs/python-version), [Flask factory with Gunicorn](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/).
