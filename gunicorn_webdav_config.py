"""gunicorn WSGI server configuration for webdav."""
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = "0.0.0.0:" + environ.get("PORT", "8081")
max_requests = 1000
workers = max_workers()
raw_env = ["APP_NAME=econtrole-webdav"]
logconfig = "./logging_webdav.conf"
timeout = 300
