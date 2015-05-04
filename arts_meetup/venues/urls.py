from django.conf.urls.defaults import *

urlpatterns = patterns ('arts_meetup.venues.views',

    (r'^(\w+)/(\w+)$', 'venue'),
    (r'^register/$', 'register'),
)
