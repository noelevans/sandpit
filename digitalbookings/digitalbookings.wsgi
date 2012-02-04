import os
import sys

from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'digitalbookings.settings'
sys.path.append('/home/noelevans/webapps/digitalbookings')
sys.path.append('/home/noelevans/webapps/digitalbookings/digitalbookings')
sys.path.append('/home/noelevans/webapps/digitalbookings/digitalbookings/bookings')

application = WSGIHandler()
