"""gunicorn WSGI server configuration for webdav."""
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = "0.0.0.0:" + environ.get("PORT", "8081")
max_requests = 1000
workers = max_workers()
raw_env = ["APP_NAME=econtrole-webdav"]
# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn_e-controle_webdav_access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn_e-controle_webdav_error.log"
# How verbose the Gunicorn error logs should be
loglevel = "error"
timeout = 300
