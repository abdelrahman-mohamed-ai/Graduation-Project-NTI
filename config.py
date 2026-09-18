from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('EDUGUARD_SECRET_KEY')
    DATABASE = os.environ.get('EDUGUARD_DATABASE_PATH') or str(BASE_DIR / 'instance' / 'eduguard.db')
    DEBUG = False
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024
    SEED_DATABASE = True
    JSON_SORT_KEYS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


def deployment_config():
    """Read deployment settings at factory creation, without changing local defaults."""
    production = os.environ.get('EDUGUARD_ENV', 'development') == 'production'
    settings = {
        'PRODUCTION': production,
        'SECRET_KEY': os.environ.get('SECRET_KEY') or os.environ.get('EDUGUARD_SECRET_KEY'),
        'DATABASE': os.environ.get('EDUGUARD_DATABASE_PATH') or Config.DATABASE,
        'SEED_DATABASE': os.environ.get('EDUGUARD_SEED_DATABASE', 'true').lower() == 'true',
        'SESSION_COOKIE_SECURE': production,
        'DEBUG': False,
    }
    if os.environ.get('DATABASE_URL'):
        raise RuntimeError('DATABASE_URL is not supported by the SQLite adapter. See DEPLOYMENT.md before configuring PostgreSQL.')
    if production and not settings['SECRET_KEY']:
        raise RuntimeError('SECRET_KEY must be supplied in production.')
    if production and not os.environ.get('EDUGUARD_DATABASE_PATH'):
        raise RuntimeError('EDUGUARD_DATABASE_PATH must point to persistent storage in production.')
    return settings
