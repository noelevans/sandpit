from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from arts_meetup.tags.models   import RoleTag
from arts_meetup.tags.views    import *


role_info_dict = {
    'queryset': RoleTag.objects.all(),
}

interests_info_dict = {
    'queryset': OtherTag.objects.all(),
}


urlpatterns = patterns ('arts_meetup.tags.views',

    (r'^/$', 'show_all'),
    (r'^maketag/$', make_tag),
    (r'^roles/$', object_list, role_info_dict), #, extra_context = { 'all_tags': Tag.objects.all() }),
    (r'^roles/(?P<name>\w+)/$', users_by_role),
    (r'^interests/$', object_list, interests_info_dict),
    (r'^interests/(?P<name>\w+)/$', users_by_interest),

)
