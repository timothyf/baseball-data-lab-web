from .base import *  # noqa
from .env import DATABASES as ENV_DATABASES

DEBUG = False

DATABASES = ENV_DATABASES
