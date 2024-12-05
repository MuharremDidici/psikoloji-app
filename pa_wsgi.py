import sys
import os

# PythonAnywhere üzerindeki proje dizinini buraya ekleyin
path = '/home/KULLANICIADI/psikoloji'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
application.secret_key = 'your-secret-key-here'

# WebSocket için gerekli WSGI middleware
from werkzeug.middleware.proxy_fix import ProxyFix
application.wsgi_app = ProxyFix(application.wsgi_app, x_for=1, x_proto=1)
