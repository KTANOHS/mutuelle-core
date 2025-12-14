
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT