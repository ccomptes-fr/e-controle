#!/bin/sh
# End of line for this file must be LF
rm -rf /var/log/celery.pid
celery multi start worker1\
        --beat -A ecc -l info\
        --scheduler=django_celery_beat.schedulers:DatabaseScheduler\
        --pidfile=/var/log/celery.pid\
        --logfile=/var/log/ecc-celery.log
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:${PORT}

