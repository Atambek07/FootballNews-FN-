"""
WSGI config for football_news project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'football_news.settings')

application = get_wsgi_application()