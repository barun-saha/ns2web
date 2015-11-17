import os
import sys

sys.path.append('/home/barun/codes/python/django/ns2')
sys.path.append('/home/barun/codes/python/django/ns2/ns2web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ns2web.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
