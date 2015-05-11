from datetime                       import date

from django.shortcuts               import get_object_or_404
from django.http                    import *
from django.views.generic           import list_detail
from django.contrib.auth.models     import User
from django.shortcuts               import render_to_response
from django.template                import RequestContext
from django.contrib.auth.decorators import login_required

from models                         import Booking
from arts_meetup.users.models       import Profile
from arts_meetup.tags.models        import *


def uk_str_to_date(uk_date):
    split_date = map(int, uk_date.split('/'))
    return date(split_date[2], split_date[1], split_date[0])


def valid_date(date):
    result = False
    try:
        uk_str_to_date(date)
        result = True
    except:
        pass
    return result


def users_by_itinerary(request, username):
    # Look up the itinerary (and raise a 404 if it can't be found).
    user = get_object_or_404(User, username__iexact=username)
    today = date.today()
    busy_today = Booking.objects.filter(
            profile=user.get_profile(),
            start__lte=today, end__gte=today
        )
    # Use the object_list view for the heavy lifting.
    return list_detail.object_list(
        request,
        queryset = Booking.objects.filter(profile__user=user),
        template_name = "booking/users_by_itinerary.html",
        template_object_name = 'booking',
        extra_context =
            {
                "h_user" :    user,
                'busy_today': busy_today,
                'all_tags':   Tag.objects.all()
            }
    )



# todo noel
# think this should be an object_detail rather than object_list func
# so should go in urls ??
def booking_by_id(request, booking_id):

#    user    = get_object_or_404(User,    username__iexact=username)
    booking = get_object_or_404(Booking, id=booking_id)
#    user = get_object_or_404(User, profile__booking__id=booking_id)
    return render_to_response(
            "booking/booking_by_id.html",
            {
                'booking':  booking,
                'all_tags': Tag.objects.all()
            },
            RequestContext(request))



@login_required
def mod_booking(request):
    errors = []
    if request.method == 'POST':
        title     = request.POST.get('title', '')
        start     = request.POST.get('start', '')
        until     = request.POST.get('until', '')
        location  = request.POST.get('location', '')
        more      = request.POST.get('more', '')
        id        = request.POST.get('id', '')
        if not title:
            errors.append('Give a name for the time booking')
        if not start:
            errors.append('Enter a start date')
        elif not valid_date(start):
            errors.append('Enter a valid start date')
            start = ''
        if not until:
            errors.append('Enter an end date')
        elif not valid_date(until):
            errors.append('Enter a valid end date')
            until = ''
        if start and until:
            start_date = uk_str_to_date(start)
            until_date   = uk_str_to_date(until)
            if start_date > until_date:
                errors.append('Start date is after the end date')
        if not errors:
            if id == '':
                b = Booking()
            else:
                b = Booking.objects.get(id=int(id))

            b.start=start_date
            b.end=until_date
            b.name=title
            b.location=location
            b.more=more
            b.profile=request.user.get_profile()
            b.save()
            request.user.get_profile().save()
            # return HttpResponseRedirect("/users/" + request.user.username)
            return HttpResponseRedirect("/booking/id/" + str(b.id) + "/")
    else:
        id_param = request.GET.get('id', '')
        # If true, is a create rather than update call
        if id_param == '':
            title    = ''
            start    = ''
            until    = ''
            more     = ''
            location = ''
            id       = ''
        else:
            try:
                booking = request.user.get_profile().booking_set.get(id=id_param)
            except:
                return HttpResponseNotFound("Booking does not correspond to this user")
            title    = booking.name
            start    = booking.start
            until    = booking.end
            more     = booking.more
            location = booking.location
            id       = id_param

    return render_to_response('booking/book_time.html', {
            'errors'  : errors,
            'title'   : title,
            'start'   : start,
            'until'   : until,
            'more'    : more,
            'location': location,
            'id'      : id,
            'all_tags': Tag.objects.all()
        }, RequestContext(request)
    )



@login_required
def delete(request, id):
    booking = get_object_or_404(Booking, id=id)
    if booking.profile == request.user.get_profile():
        booking.delete()
        return HttpResponseRedirect(
                '/booking/' + request.user.get_profile().name + '/'
            )
    return HttpResponseForbidden()
