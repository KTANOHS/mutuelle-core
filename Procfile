# Procfile pour Render.com
web: gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile - --error-logfile -
release: python manage.py migrate --noinput
worker: python manage.py process_tasks