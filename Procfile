web: python manage.py migrate && gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
release: python manage.py migrate
