import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def now(): return datetime.now(timezone.utc).isoformat(timespec='microseconds')


class StudentRepository:
    def __init__(self, path):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript('''
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY, student_uid TEXT UNIQUE NOT NULL,
                    student_name TEXT, course_code INTEGER, source TEXT NOT NULL,
                    features_json TEXT NOT NULL, risk_probability REAL, risk_level TEXT,
                    manual_review INTEGER, created_at TEXT, updated_at TEXT, last_analyzed_at TEXT);
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL REFERENCES students(id),
                    risk_probability REAL, risk_level TEXT, manual_review INTEGER,
                    result_json TEXT NOT NULL, model_stage TEXT, created_at TEXT);
                CREATE TABLE IF NOT EXISTS data_imports (
                    id INTEGER PRIMARY KEY, filename TEXT, row_count INTEGER,
                    success_count INTEGER, failed_count INTEGER, created_at TEXT);
                CREATE TABLE IF NOT EXISTS import_batches (
                    token TEXT PRIMARY KEY, session_id TEXT NOT NULL, filename TEXT,
                    payload_json TEXT NOT NULL, created_at TEXT, status TEXT DEFAULT 'preview', result_json TEXT);
                CREATE INDEX IF NOT EXISTS idx_risk ON students(risk_level, course_code);
                CREATE INDEX IF NOT EXISTS idx_history ON analysis_history(student_id, id DESC);
            ''')

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally: db.close()

    def decode(self, row):
        if row is None: return None
        d = dict(row)
        d['features'] = json.loads(d.pop('features_json'))
        d['manual_review'] = bool(d['manual_review'])
        d['risk_score'] = round(d['risk_probability'] * 100, 2) if d['risk_probability'] is not None else None
        return d

    def count(self):
        with self.connection() as db: return db.execute('SELECT count(*) FROM students').fetchone()[0]

    def get(self, uid):
        with self.connection() as db:
            d = self.decode(db.execute('SELECT * FROM students WHERE student_uid=?', (uid,)).fetchone())
            if d:
                d['history'] = [dict(r) for r in db.execute('SELECT id, result_json, created_at FROM analysis_history WHERE student_id=? ORDER BY id DESC LIMIT 100', (d['id'],))]
                for h in d['history']: h['result'] = json.loads(h.pop('result_json'))
                d['result'] = d['history'][0]['result'] if d['history'] else None
            return d

    def query(self, filters=None, page=1, per_page=20, all_rows=False):
        filters = filters or {}
        where, params = [], []
        if filters.get('q'):
            where.append('(student_uid LIKE ? ESCAPE "\\" OR student_name LIKE ? ESCAPE "\\")')
            q = '%' + filters['q'].replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
            params.extend([q, q])
        for key, col in [('risk', 'risk_level'), ('course', 'course_code'), ('source', 'source')]:
            if filters.get(key): where.append(f'{col}=?'); params.append(filters[key])
        if filters.get('review') in ('0', '1'):
            where.append('manual_review=?'); params.append(int(filters['review']))
        for key, op in [('min_risk', '>='), ('max_risk', '<=')]:
            if filters.get(key) not in (None, ''):
                value = float(filters[key])
                if not 0 <= value <= 100: raise ValueError('Risk range must be between 0 and 100.')
                where.append(f'risk_probability {op} ?'); params.append(value / 100)
        if filters.get('date'):
            datetime.strptime(filters['date'], '%Y-%m-%d')
            where.append('substr(last_analyzed_at,1,10)=?'); params.append(filters['date'])
        if filters.get('uids'):
            where.append('student_uid IN (' + ','.join('?' for _ in filters['uids']) + ')'); params.extend(filters['uids'])
        clause = ' WHERE ' + ' AND '.join(where) if where else ''
        sort = {'risk': 'risk_probability', 'id': 'student_uid', 'name': 'student_name', 'course': 'course_code', 'date': 'last_analyzed_at'}.get(filters.get('sort'), 'risk_probability')
        direction = 'ASC' if filters.get('direction') == 'asc' else 'DESC'
        with self.connection() as db:
            total = db.execute('SELECT count(*) FROM students' + clause, params).fetchone()[0]
            sql = 'SELECT * FROM students' + clause + f' ORDER BY {sort} {direction}, student_uid ASC'
            if not all_rows: sql += ' LIMIT ? OFFSET ?'; params += [per_page, (page - 1) * per_page]
            return {'students': [self.decode(r) for r in db.execute(sql, params)], 'total': total, 'page': page, 'per_page': per_page}

    def insert_result(self, db, uid, name, source, result):
        stamp = now()
        if not uid:
            n = db.execute('SELECT COALESCE(MAX(id),0)+1 FROM students').fetchone()[0]
            uid = f'STU-{n:06d}'
            while db.execute('SELECT 1 FROM students WHERE student_uid=?', (uid,)).fetchone(): n += 1; uid = f'STU-{n:06d}'
        cursor = db.execute('''INSERT INTO students(student_uid,student_name,course_code,source,features_json,
            risk_probability,risk_level,manual_review,created_at,updated_at,last_analyzed_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
            (uid, name or None, result['features']['Course'], source, json.dumps(result['features']), result['risk_probability'],
             result['risk_level'], int(result['manual_review']), stamp, stamp, stamp))
        self.history(db, cursor.lastrowid, result, stamp)
        return uid

    def history(self, db, student_id, result, stamp):
        db.execute('INSERT INTO analysis_history(student_id,risk_probability,risk_level,manual_review,result_json,model_stage,created_at) VALUES(?,?,?,?,?,?,?)',
            (student_id, result['risk_probability'], result['risk_level'], int(result['manual_review']), json.dumps(result), result['model_stage'], stamp))

    def save(self, uid, name, source, result):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            return self.insert_result(db, uid, name, source, result)

    def analyze(self, uid, result):
        with self.connection() as db:
            row = db.execute('SELECT id FROM students WHERE student_uid=?', (uid,)).fetchone()
            if not row: raise KeyError(uid)
            stamp = now()
            db.execute('UPDATE students SET risk_probability=?,risk_level=?,manual_review=?,last_analyzed_at=?,updated_at=? WHERE id=?',
                (result['risk_probability'], result['risk_level'], int(result['manual_review']), stamp, stamp, row['id']))
            self.history(db, row['id'], result, stamp)

    def seed(self, model):
        if self.count() or not model.ready: return 0
        import pandas as pd
        path = model.root / 'artifacts' / 'enrolled_students_risk_scores.csv'
        if path.exists():
            frame = pd.read_csv(path); frame.columns = frame.columns.str.strip()
        else: frame = model.source
        if not set(model.features).issubset(frame.columns): frame = model.source
        if 'Target' not in frame or not set(model.features).issubset(frame.columns): return 0
        frame = frame.loc[frame['Target'] == 'Enrolled', model.features]
        results = model.predict_many(frame.to_dict('records'))
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT count(*) FROM students').fetchone()[0]: return 0
            for i, result in enumerate(results, 1): self.insert_result(db, f'STU-{i:06d}', None, 'Enrolled dataset', result)
        return len(results)
