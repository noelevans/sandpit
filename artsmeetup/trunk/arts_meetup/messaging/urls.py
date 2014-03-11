from django.conf.urls.defaults          import *
from django.contrib.auth.views          import logout
from django.views.generic.list_detail   import object_detail
from django.views.generic.create_update import create_object

from arts_meetup.messaging.models import Message
from views  import *


urlpatterns = patterns ('arts_meetup.messaging.views',

    (r'^create_msg/.*$', create_msg),
    (r'^delete_msg/(\d+)/$', delete_msg),
#    (r'^create/$', create_object, dict(
#        model=Message,
#        login_required=True,
#        post_save_redirect="/accounts/whoami/")),
    (r'^(\w+)/$', msgs_by_user),

)
