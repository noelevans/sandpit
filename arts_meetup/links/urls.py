from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns ('arts_meetup.links.views',

    (r'^add/$',           add),
    (r'^delete/(\d+)/$',  delete),
    (r'^(\w+)/$',         user_links),

)
