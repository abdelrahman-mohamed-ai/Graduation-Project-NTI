import csv
import io
import json
import logging
import secrets
import sqlite3
from functools import lru_cache
from flask import Flask, jsonify, render_template, request, session, Response, abort
from werkzeug.exceptions import HTTPException
from config import BASE_DIR, Config, deployment_config
from services.model_service import ModelService, ValidationError, group_for, friendly
from services.import_service import ImportService, identity
from services.dashboard_service import dashboard
from repositories.student_repository import StudentRepository
from services.i18n_service import init_i18n
from services.presentation_service import presentation_payload


@lru_cache(maxsize=1)
def loaded_model(): return ModelService(BASE_DIR)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(deployment_config())
    if test_config: app.config.update(test_config)
    if app.config.get('PRODUCTION'):
        app.config.update(DEBUG=False, PROPAGATE_EXCEPTIONS=False)
    app.json.sort_keys = False
    init_i18n(app)
    if not app.config.get('SECRET_KEY'):
        secret_path = BASE_DIR / 'instance' / '.session-secret'
        secret_path.parent.mkdir(exist_ok=True)
        try:
            with secret_path.open('x') as secret_file: secret_file.write(secrets.token_hex(32))
        except FileExistsError: pass
        app.config['SECRET_KEY'] = secret_path.read_text().strip()
    model = loaded_model()
    repo = StudentRepository(app.config['DATABASE'])
    importer = ImportService(model, repo)
    app.extensions.update(model_service=model, student_repository=repo, import_service=importer)
    if app.config['SEED_DATABASE']:
        try: app.logger.info('Seeded %s current students', repo.seed(model))
        except Exception: app.logger.exception('Unable to seed students; original data remains intact')

    @app.before_request
    def security():
        session.setdefault('csrf', secrets.token_urlsafe(32))
        session.setdefault('sid', secrets.token_urlsafe(24))
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            token = request.headers.get('X-CSRF-Token', '')
            if not secrets.compare_digest(token, session['csrf']): return jsonify(error='Session verification failed. Refresh the page and try again.'), 403

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'same-origin'
        if app.config.get('PRODUCTION'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000'
        if request.path.startswith('/api/') or request.path.startswith('/exports/'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    @app.context_processor
    def context():
        return dict(model=model, csrf_token=session.get('csrf', ''), friendly=friendly, group_for=group_for,
                    nav=[('dashboard', '/', 'layout-dashboard', 'Dashboard'), ('students', '/students', 'users', 'Students'),
                         ('analyze', '/analyze', 'scan-line', 'Analyze Risk'), ('upload', '/upload', 'upload-cloud', 'Upload Data'),
                         ('model_page', '/model', 'brain-circuit', 'Model Insights'), ('dataset', '/dataset', 'database', 'Dataset & Features'),
                         ('reports', '/reports', 'file-chart-column', 'Reports'), ('powerpoint', '/powerpoint', 'presentation', 'PowerPoint'),
                         ('about', '/about', 'info', 'About Project')])

    def with_course(s):
        s['course_name'] = model.course(s['course_code'])
        return s

    def get_student(uid):
        student = repo.get(uid)
        if not student: abort(404, description='Student not found.')
        return with_course(student)

    def data():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict): raise ValidationError({'form': 'Send a valid JSON object.'})
        return payload

    @app.get('/')
    @app.get('/dashboard')
    def dashboard_page(): return render_template('dashboard.html', title='Dashboard', page='dashboard')

    @app.get('/students')
    def students(): return render_template('students.html', title='Students', page='students')

    @app.get('/students/<student_id>')
    def student_detail(student_id):
        student = get_student(student_id)
        return render_template('student_detail.html', title='Student profile', page='students', student=student)

    @app.get('/analyze')
    def analyze(): return render_template('analyze.html', title='Analyze Risk', page='analyze', schema=model.schema)

    @app.get('/upload')
    def upload(): return render_template('upload.html', title='Upload Data', page='upload')

    @app.get('/dataset')
    def dataset():
        counts = model.source['Target'].value_counts().to_dict() if 'Target' in model.source else {}
        return render_template('dataset.html', title='Dataset & Features', page='dataset', counts=counts, dictionary=model.dictionary)

    @app.get('/model')
    def model_page(): return render_template('model.html', title='Model Insights', page='model_page')

    @app.get('/reports')
    def reports():
        with repo.connection() as db: imports = [dict(r) for r in db.execute('SELECT * FROM data_imports ORDER BY id DESC LIMIT 20')]
        return render_template('reports.html', title='Reports', page='reports', imports=imports)

    @app.get('/about')
    def about(): return render_template('about.html', title='About Project', page='about')

    @app.get('/powerpoint')
    def powerpoint(): return render_template('powerpoint.html', title='PowerPoint', page='powerpoint', presentation=presentation_payload(model))

    @app.get('/health')
    def health(): return jsonify(status='ok')

    @app.get('/api/dashboard')
    def api_dashboard(): return jsonify(dashboard(repo, model))

    @app.get('/api/students')
    def api_students():
        page_number = max(1, int(request.args.get('page', 1)))
        per_page = max(1, min(100, int(request.args.get('per_page', 20))))
        result = repo.query(request.args, page_number, per_page)
        result['students'] = [with_course(s) for s in result['students']]
        return jsonify(result)

    @app.get('/api/students/search')
    def search():
        rows = repo.query({'q': request.args.get('q', '')[:160], 'sort': 'id', 'direction': 'asc'}, per_page=12)['students']
        return jsonify(students=[with_course(s) for s in rows])

    @app.get('/api/students/<student_id>')
    def api_student(student_id): return jsonify(get_student(student_id))

    @app.post('/api/analyze/<student_id>')
    def analyze_existing(student_id):
        student = get_student(student_id)
        result = model.predict(student['features'])
        repo.analyze(student_id, result)
        return jsonify(result=result, student_uid=student_id)

    @app.post('/api/analyze/manual')
    def analyze_manual():
        payload = data()
        identity(payload)
        return jsonify(result=model.predict(payload.get('features', payload)))

    @app.post('/api/students')
    def save_student():
        payload = data()
        uid, name = identity(payload)
        result = model.predict(payload.get('features', payload))
        uid = repo.save(uid, name, 'Manual entry', result)
        return jsonify(student_uid=uid, result=result), 201

    @app.get('/api/sample')
    def sample():
        if model.source.empty: return jsonify(error=model.dataset_error or 'Source dataset unavailable.'), 503
        # One complete, actual source row; do not build a synthetic median student.
        row = model.source.loc[model.source['Target'] == 'Enrolled'].iloc[0]
        return jsonify(features=model.validate(row[model.features].to_dict()), provenance='First Enrolled row in original data.csv; name and local ID are not source fields.')

    @app.post('/api/upload')
    def api_upload():
        model.ensure_ready()
        if 'file' not in request.files: raise ValueError('Choose a CSV or XLSX file.')
        return jsonify(importer.preview(request.files['file'], session['sid']))

    @app.post('/api/upload/commit')
    def commit_upload(): return jsonify(importer.commit(data().get('token', ''), session['sid']))

    def csv_response(rows, filename, fields=None):
        output = io.StringIO(newline='')
        fields = fields or (list(rows[0]) if rows else ['Student ID', 'Student Name', 'Risk Score', 'Risk Level', 'Manual Review Recommended'])
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            # Neutralize spreadsheet formulas in user-controlled text, preserving numerical values.
            safe = {k: ("'" + v if isinstance(v, str) and v.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else v) for k, v in row.items()}
            writer.writerow(safe)
        return Response('\ufeff' + output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename="{filename}"'})

    @app.get('/exports/template.csv')
    def template_csv(): return csv_response([], 'eduguard-import-template.csv', ['Student ID', 'Student Name'] + model.features)

    @app.get('/exports/students.csv')
    def export_students():
        filters = request.args.to_dict()
        if filters.get('batch'):
            with repo.connection() as db:
                batch = db.execute("SELECT result_json FROM import_batches WHERE token=? AND session_id=? AND status='complete'", (filters['batch'], session['sid'])).fetchone()
            if not batch: abort(404)
            uids = json.loads(batch['result_json'])['student_uids']
            if not uids: return csv_response([], 'eduguard-students.csv')
            filters['uids'] = uids
        rows = repo.query(filters, all_rows=True)['students']
        result = [{'Student ID': s['student_uid'], 'Student Name': s['student_name'] or '', 'Course Name': model.course(s['course_code']),
                   'Risk Score': s['risk_score'], 'Risk Level': s['risk_level'], 'Manual Review Recommended': 'Yes' if s['manual_review'] else 'No',
                   'Last Analysis': s['last_analyzed_at'], **s['features']} for s in rows]
        return csv_response(result, 'eduguard-students.csv')

    @app.get('/exports/summary.csv')
    def export_summary():
        rows = repo.query(request.args, all_rows=True)['students']
        summary = []
        for level in ['High', 'Medium', 'Low']:
            selected = [s for s in rows if s['risk_level'] == level]
            summary.append({'Risk Level': level, 'Students': len(selected), 'Average Risk (%)': round(sum(s['risk_score'] for s in selected) / len(selected), 2) if selected else '', 'Manual Review': sum(s['manual_review'] for s in selected)})
        return csv_response(summary, 'eduguard-risk-summary.csv')

    @app.errorhandler(Exception)
    def errors(exc):
        status, message, fields = 500, 'Something went wrong. Please try again. If this continues, check the application log.', {}
        if isinstance(exc, ValidationError): status, message, fields = 422, str(exc), exc.errors
        elif isinstance(exc, sqlite3.IntegrityError): status, message = 409, 'This student ID already exists. Choose a unique ID.'
        elif isinstance(exc, ValueError): status, message = 400, str(exc)
        elif isinstance(exc, HTTPException):
            status = exc.code
            message = 'The upload exceeds the 15 MB limit.' if status == 413 else exc.description
        elif isinstance(exc, RuntimeError) and not model.ready: status, message = 503, model.error
        else: app.logger.exception('Request failed')
        if request.path.startswith('/api/') or request.path.startswith('/exports/'): return jsonify(error=message, errors=fields), status
        return render_template('error.html', title='Unable to open page', page='', status=status, message=message), status

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    create_app().run(host='127.0.0.1', port=5000, debug=False)
