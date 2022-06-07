#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
celery multi start worker1\
        --beat -A ecc -l info\
        --scheduler=django_celery_beat.schedulers:DatabaseScheduler\
        --pidfile=/var/log/celery.pid\
        --logfile=/var/log/ecc-celery.log
gunicorn -c gunicorn_config.py ecc.wsgi:application
