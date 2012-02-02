from django.shortcuts                 import get_object_or_404
from django.views.generic.list_detail import object_detail
from tridates.regions.models          import Region
from tridates.events.models           import Event


def events_by_region(request, object_id, queryset):
    req_region = get_object_or_404(Region, id=object_id)
    return object_detail(
        request,
        queryset=queryset,
        object_id = object_id,
        extra_context = {"events" : Event.objects.filter(region=req_region)}
    )


