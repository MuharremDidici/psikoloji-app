import multiprocessing

# Gunicorn yapılandırması
bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "eventlet"
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# SSL/TLS yapılandırması
keyfile = None
certfile = None

# WebSocket yapılandırması
websocket_ping_interval = 25
websocket_ping_timeout = 60

# İşlem yönetimi
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Güvenlik
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
