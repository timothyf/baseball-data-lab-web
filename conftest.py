import os
import django
from django.test.utils import setup_test_environment, teardown_test_environment, setup_databases, teardown_databases
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseball_data_lab_web.settings.test')
django.setup()

# @pytest.fixture(scope='session', autouse=True)
# def django_test_environment():
#     """Set up and tear down the Django test environment."""
#     setup_test_environment()
#     old_config = setup_databases(verbosity=0, interactive=False)
#     yield
#     teardown_databases(old_config, verbosity=0)
#     teardown_test_environment()
