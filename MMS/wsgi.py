"""
WSGI config for MMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/data/www/rnai.pfizer.com/django-MMS')
sys.path.append('/data/www/rnai.pfizer.com')
sys.path.append('/data/www/rnai.pfizer.com/django-MMS/MMS')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MMS.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "MMS.settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


