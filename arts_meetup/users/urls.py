from django.conf.urls.defaults        import *
from django.views.generic.list_detail import object_detail, object_list

from models                           import Profile
from views                            import *

user_info_dict = {
    'queryset':      Profile.objects.all(),
    'template_name': 'profile_list.html'
}

contact_info_dict = {
    'queryset':      Profile.objects.all(),
    'template_name': 'contact_list.html'
}

urlpatterns = patterns ('arts_meetup.users.views',

    (r'^amibusy/$',                     'am_i_busy'),
    (r'^add_interests/$',               'add_interests'),
    (r'^remove_interests/$',            'remove_interests'),
    (r'^add_roles/$',                   'add_roles'),
    (r'^remove_roles/$',                'remove_roles'),
    (r'^add_friends/$',                 'add_friends'),
    (r'^remove_friends/$',              'remove_friends'),
    (r'^maketag/$',                     'maketag'),
    (r'^$',                             object_list, user_info_dict),
    (r'^all/$',                         'show_all'),
    (r'^all/ppl$',                      'show_all'),
    (r'^all/groups$',                   'show_all'),
    (r'^all/venues$',                   'show_all'),
    (r'^(\w+)/contacts/$',              contacts),
    (r'^(\w+)/contacts/remove/(\w+)/$', remove_contact),
    (r'^(\w+)/contacts/add/(\w+)/$',    add_contact),
    (r'^(\w+)/$',                       'user'),

)
