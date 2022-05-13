#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0:${PORT}
celery multi start worker1\
        --beat -A ecc -l info\
        --scheduler=django_celery_beat.schedulers:DatabaseScheduler\
        --pidfile=/var/run/celery/celery.pid\
        --logfile=/var/log/ecc-celery.log