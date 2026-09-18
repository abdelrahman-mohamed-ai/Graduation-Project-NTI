"""Single SQLite instance; keep ML memory bounded. Linux production only."""
import os
bind = '0.0.0.0:' + os.environ.get('PORT', '8000')
workers = 1
worker_class = 'gthread'
threads = 4
timeout = 180
graceful_timeout = 180
accesslog = '-'
errorlog = '-'
capture_output = True
reload = False
