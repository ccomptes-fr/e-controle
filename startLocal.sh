#!/bin/sh
# End of line for this file must be LF
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:${PORT}
celery multi start worker1\
        --beat -A ecc -l info\
        --scheduler=django_celery_beat.schedulers:DatabaseScheduler\
        --pidfile=\
        --logfile=/var/log/ecc-celery.log
