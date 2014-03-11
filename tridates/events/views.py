import datetime
from datetime                            import *
from django.views.generic.create_update  import create_object
from django.shortcuts                    import render_to_response
from django.contrib.auth.decorators      import login_required
from django.http                         import HttpResponseRedirect
from django.views.generic.list_detail    import object_list
from django.db.models                    import Count
from django.views.decorators.csrf        import csrf_protect
from django.contrib                      import auth

from tridates.events.models              import Event
from tridates.regions.models             import Region
from tridates.events.forms               import EventForm, UserCreationFormWithEmail


def home(request):
    next_event = Event.objects.filter(start_date__gt=datetime.today())[0]
    next_event_wait = (next_event.start_date - date.today()).days
    return render_to_response(
        'events/home.html',
        {'last_added': Event.objects.filter().reverse()[:3],
         'next_event': next_event,
         'next_event_wait': next_event_wait,
         'event_count_2010': Event.objects.filter(start_date__year=2010).count(),
         'event_count_2011': Event.objects.filter(start_date__year=2011).count(),
         'event_count_2012': Event.objects.filter(start_date__year=2012).count(),
         'active_regions': Region.objects.annotate(
             region_events=Count('event')),
       },
    )

#@csrf_response_exempt
@csrf_protect
def register(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password1'])
            auth.login(request, user)
            #print "1: " + form.cleaned_data['next']
            #next = form.cleaned_data.get('next', '/')
            #print "2: " + str(form.cleaned_data.get('next', '/'))
            return HttpResponseRedirect("/events/create")
    else:
        form = UserCreationFormWithEmail()
    c['form'] = form
    return render_to_response(
        'registration/register.html',
        c,
        #{'form': form}, 
        context_instance=RequestContext(request),
    )
    
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.added_by = request.user
            new_event.save()
            new_event.disciplines = form.cleaned_data['disciplines'].all()
            new_event.status = form.cleaned_data['status']
            new_event.save()
            return HttpResponseRedirect('/events/' + str(new_event.id))
    else:
        form = EventForm()
    return render_to_response(
        'events/event_form.html', 
        {'form': form},
    )

def events_by_year(request, year):
    return object_list(
        request,
        Event.objects.filter(start_date__year=year),
        #extra_context = {"events" : Event.objects.filter(start_date__year=year)}
    )

