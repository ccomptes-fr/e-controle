#!/bin/sh
gunicorn -c gunicorn_webdav_config.py webdav.wsgi:application