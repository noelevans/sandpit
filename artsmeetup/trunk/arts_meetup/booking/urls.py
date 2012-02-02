from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from arts_meetup.booking.models   import Booking
from arts_meetup.booking.views    import *


info_dict_all = {
    'queryset': Booking.objects.all(),
}


urlpatterns = patterns ('arts_meetup.views',

#    (r'^/$', object_list, info_dict_all),
    (r'^book_time/$',               mod_booking),
    (r'^mod_booking/$',             mod_booking),
    (r'^delete/(\d+)/$',            delete),
    (r'^id/(?P<booking_id>\d+)/$',  booking_by_id),
    (r'^(?P<username>\w+)/$',       users_by_itinerary),

)
