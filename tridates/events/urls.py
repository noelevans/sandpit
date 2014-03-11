from django.conf.urls.defaults import *
from tridates.events.models    import *
from tridates.events.views     import *

info_dict = {
    'queryset': Event.objects.all(),
}

urlpatterns = patterns('',

    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    (r'^year/(\d+)/$', events_by_year),
    (r'^create/$', create_event),
    
    #url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='events/results.html'), 'events_results'),
    #(r'^(?P<event_id>\d+)/vote/$', 'tridates.events.views.vote'),
)
