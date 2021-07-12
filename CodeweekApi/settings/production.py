from .base import *

from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['localhost']


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
