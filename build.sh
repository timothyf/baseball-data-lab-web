pip install -r backend/requirements.txt \
 && cd frontend && npm ci && npm run build && cd .. \
 && python backend/manage.py collectstatic --noinput
