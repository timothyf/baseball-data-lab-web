pip install -r backend/requirements.txt \
 && cd frontend && npm ci && npm run build && cd .. \
 && DJANGO_SETTINGS_MODULE=baseball_data_lab_web.settings.prod python backend/manage.py collectstatic --noinput
