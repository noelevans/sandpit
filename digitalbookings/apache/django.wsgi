import django.core.handlers.wsgi
import os
import sys

sys.path.append('/home/eric/Python/PROJECT')
os.environ['DJANGO_SETTINGS_MODULE'] = 'PROJECT.settings'
application = django.core.handlers.wsgi.WSGIHandler()
