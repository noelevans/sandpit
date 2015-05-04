from django.conf.urls.defaults  import *
from django.conf                import settings
from django.contrib             import admin
admin.autodiscover()

from arts_meetup.feeds          import LatestEntries

feeds = {
    'latest': LatestEntries,
#    'categories': LatestEntriesByCategory,
}


urlpatterns = patterns('',

    (r'^blog/',             include('arts_meetup.blog.urls')),
    (r'^accounts/',         include('arts_meetup.accounts.urls')),
    (r'^venues/',           include('arts_meetup.venues.urls')),
    (r'^users/',            include('arts_meetup.users.urls')),
    (r'^links/',            include('arts_meetup.links.urls')),
    (r'^tags/',             include('arts_meetup.tags.urls')),
    (r'^booking/',          include('arts_meetup.booking.urls')),
    (r'^msging/',           include('arts_meetup.messaging.urls')),
    (r'^home/',             'arts_meetup.accounts.views.send_home'),
    (r'^$',                 'arts_meetup.accounts.views.send_home'),
    (r'^feeds/(?P<url>.*)', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),


)
