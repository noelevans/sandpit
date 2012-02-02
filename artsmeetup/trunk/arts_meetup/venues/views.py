from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Venue
from forms  import VenueRegistrationForm


def venue(request, city, name):
    # This outlines the DB interfaces implemented
    # file:///home/noel/Desktop/Django-1.0.2-final/docs/_build/html/topics/db/queries.html
    # eg ....  city__iexact=city   -- test match, case INsensitive
    v = Venue.objects.get(city__exact=city)    # do city test also
    context_instance=RequestContext(request)

    if len(v.contact.filter(username=request.user.username)) > 0 :
        is_venue_contact = True
    else:
        is_venue_contact = False
    return render_to_response(
        'venue_home.html',
        { 'venue': v, 'is_venue_contact': is_venue_contact},
        RequestContext(request))


""" View to register a venue. Note that you must be
logged in to carry out the registration """
@login_required
def register(request):
    if request.method == 'POST':
        form = VenueRegistrationForm(request.POST)

        if form.is_valid():
            v = Venue()
            v.name            = form.cleaned_data['name']
            v.venue_type      = form.cleaned_data['venue_type']
            v.address_line_1  = form.cleaned_data['address_line_1']
            v.address_line_2  = form.cleaned_data['address_line_2']
            v.website         = form.cleaned_data['website']
            v.telephone       = form.cleaned_data['telephone']
            v.city            = form.cleaned_data['city']
            v.capacity        = form.cleaned_data['capacity']
            v.producing       = form.cleaned_data['producing']
            v.recieving       = form.cleaned_data['recieving']
            # Have to save before we can add the venue_contact
            print("Just about to save Venue")
            v.save()
            print("Saved Venue. Adding Venue to Contact")
            # Now associate the contact
            v.contact.add(request.user)
            print("Finished register_venue")


            return HttpResponseRedirect('/blog')
        else :      # this else is effectively debugging
            print(form.errors)
    else:
        form = VenueRegistrationForm()

    return render_to_response(
        'register_venue.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))

