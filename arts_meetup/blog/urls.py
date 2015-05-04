from django.conf.urls.defaults import *

from arts_meetup.blog.views    import *


urlpatterns = patterns('arts_meetup.blog.views',

    (r'^create/$',       create),
    (r'^delete/(\d+)/$', delete),
    (r'^/$',             archive),

)
