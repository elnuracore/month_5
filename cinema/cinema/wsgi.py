"""
WSGI config for cinema project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""
import dotenv
import os

from django.core.wsgi import get_wsgi_application
import os
from django.core.wsgi import get_wsgi_application
import dotenv # If you are using dotenv here too

# If you want to load env vars for the web server:
# dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

application = get_wsgi_application()

# dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

# application = get_wsgi_application()
