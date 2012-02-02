from django.conf.urls.defaults        import *
from django.views.generic.list_detail import *

from tridates.regions.models          import Region
from tridates.regions.views           import *


info_dict = {
    'queryset': Region.objects.all(),
}

urlpatterns = patterns('',

    (r'^$',                    object_list,   info_dict),
    (r'^(?P<object_id>\d+)/$', events_by_region, info_dict),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    #url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='regions/results.html'), 'regions_results'),
    #(r'^(?P<region_id>\d+)/vote/$', 'tridates.regions.views.vote'),
)
