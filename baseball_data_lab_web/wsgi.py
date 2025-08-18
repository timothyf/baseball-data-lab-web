import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseball_data_lab_web.settings')

application = get_wsgi_application()
