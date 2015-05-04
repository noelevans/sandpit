from django.conf.urls.defaults import *
from django.contrib.auth.views import logout

from views import *

urlpatterns = patterns ('arts_meetup.accounts.views',

    # while you are looking at the login, logout methods, in
    # django.contrib.auth.views there are also change-password methods
    # Also docs.djangoproject.com/en/dev/topics/auth/?from=olddocs#django.contrib.auth.django.contrib.auth.views.logout_then_login

    (r'^settings/$',            settings),
    (r'^register/individual/$', register, {'acc_type': Profile.PERSON}),
    (r'^register/venue/$',      register, {'acc_type': Profile.VENUE}),
    (r'^register/company/$',    register, {'acc_type': Profile.GROUP}),
    (r'^logout/$',              logout),
    (r'^bio/$',                 bio),
    (r'^user_picture/$',        change_image),
    (r'^whoami/$',              whoami),
    (r'^send_email/$',          is_send_email),
    (r'^$',                     login),
    (r'^login/$',               login),
    (r'^change_password/$',     change_password),
    (r'^mini_search/$',         mini_search),
    (r'^full_search/$',         full_search),
    (r'^home/$',                send_home),

)
