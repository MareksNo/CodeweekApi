from .base import *

from dotenv import load_dotenv


import cloudinary, cloudinary_storage

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['localhost', 'codeweekapi.herokuapp.com', '127.0.0.1']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'mareks',
    'API_KEY': 459214395334741,
    'API_SECRET': 'FahupuCIPe6C4m6cIOmT1Ak4wHQ',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Sentry setup
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    send_default_pii=True
)
