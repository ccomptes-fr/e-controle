#!/bin/sh
# End of line for this file must be LF
python manage.py createcachetable
gunicorn -c gunicorn_webdav_config.py webdav.wsgi:application
