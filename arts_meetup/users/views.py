import re
import datetime
from datetime                       import date

from django.forms.util              import ErrorDict
from django.shortcuts               import get_object_or_404
from django.http                    import *
from django.shortcuts               import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from django.template                import RequestContext
from datetime                       import date

from models                         import Profile
from arts_meetup.messaging.models   import Message
from arts_meetup.links.models       import URL
from arts_meetup.booking.models     import Booking
from forms                          import *



def user(request, user_name):

    h_user = get_object_or_404(User, username__iexact=user_name)
    is_my_profile = user_name == request.user.username
    if request.user.is_authenticated():
        is_friend = request.user.get_profile().contacts.filter(name=user_name)
    else:
        is_friend = False
    today = date.today()
    future_bookings = h_user.get_profile().booking_set.filter(
            end__gte=today).order_by('start')[:3]
    age = ''
    my_links = URL.objects.filter(user=h_user.get_profile())
    busy_today = Booking.objects.filter(
            profile=h_user.get_profile(), start__lte=today, end__gte=today)

    return render_to_response(
        'user_home.html',
        {
            'h_user':           h_user,
            'future_bookings':  future_bookings,
            'msg_count':        Message.objects.filter(
                                  owner=h_user, recipient=h_user).count(),
            'my_links':         my_links,
            'all_tags':         Tag.objects.all(),
            'is_my_profile':    is_my_profile,
            'is_friend':        is_friend,
            'busy_today':       bool(busy_today),
        },
        RequestContext(request))



def am_i_busy(request):
    today = date.today()
    my_events = Booking.objects.filter(profile=request.user.get_profile())
    busy_today = Booking.objects.filter(
        profile=request.user.get_profile(), start__lte=today, end__gte=today)
    return HttpResponse(
        "My events: " + str(list(my_events)) + \
        "\n\nToday (" + str(today) + "): " + str(bool(busy_today)))



@login_required
def add_friends(request):
    if request.method == 'POST':
        form = AddFriendsForm(request, request.POST)
        print(form.errors)
        if form.is_valid():
            up = request.user.get_profile()
            # get all of form data and add as applicable
            new_friends = form.cleaned_data['new_friends']
            for f in new_friends:
                up.friends.add(f)
            up.save()
            request.user.message_set.create(
                message="New friends added!")
            return HttpResponseRedirect("/users/" + request.user.username)
        else:
            # invalid form
            print("Errors: " + str(form.errors))
    else:
        form = AddFriendsForm(request)
    return render_to_response(
        'add_friends.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))


@login_required
def remove_friends(request):
    if request.method == 'POST':
        form = RemoveFriendForm(request, request.POST)
        print(form.errors)
        if form.is_valid():
            up = request.user.get_profile()
            # get all of form data and remove as applicable
            to_go_friends = form.cleaned_data['to_go_friends']
            for f in to_go_friends:
                up.friends.remove(f)
            up.save()
            return HttpResponseRedirect("/users/" + request.user.username)
        else:
            # invalid form
            print("Errors: " + form.errors)
    else:
        form = RemoveFriendsForm(request)
    return render_to_response(
        'remove_friends.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))


@login_required
def add_roles(request):
    if request.method == 'POST':
        form = AddRoleForm(request, request.POST)

        # check that the person doesn't have more than X tags added
        existing = request.user.get_profile().role.all().count()
        if form.is_valid():
            new_roles = form.cleaned_data['new_roles']
            if len(new_roles) + existing > Tag.MAX_TAGS:
                form.errors['new_roles'] = "Too many roles selected. Maximum is " + Tag.MAX_TAGS

        if form.is_valid():
            up = request.user.get_profile()
            # get all of form data and add as applicable
            new_roles = form.cleaned_data['new_roles']
            for r in new_roles:
                if Profile.VENUE == up.type:
                    up.venue_tags.add(r)
                elif Profile.GROUP == up.type:
                    up.group_tags.add(r)
                else:
                    up.role.add(r)
            up.save()
            return HttpResponseRedirect("/users/" + request.user.username)
        else:
            return HttpResponseRedirect("/users/" + request.user.username)
    else:
        form = AddRoleForm(request)
    return render_to_response(
        'add_role.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))


@login_required
def remove_roles(request):
    if request.method == 'POST':
        form = RemoveRoleForm(request, request.POST)
        print(form.errors)
        if form.is_valid():
            up = request.user.get_profile()
            # get all of form data and remove as applicable
            to_go_roles = form.cleaned_data['to_go_roles']
            for r in to_go_roles:
                if Profile.VENUE == up.type:
                    up.venue_tags.remove(r)
                elif Profile.GROUP == up.type:
                    up.group_tags.remove(r)
                else:
                    up.role.remove(r)
            up.save()
            return HttpResponseRedirect("/users/" + request.user.username)
        else:
            # invalid form
            print("Errors: " + form.errors)
    else:
        form = RemoveRoleForm(request)
    return render_to_response(
        'remove_role.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))



@login_required
def add_interests(request):
    if request.method == 'POST':
        form = AddInterestsForm(request, request.POST)
        print(form.errors)
        if form.is_valid():
            up = request.user.get_profile()
            # get all of form data and add as applicable
            new_interests = form.cleaned_data['new_interests']
            for i in new_interests:
                up.other_tags.add(i)
            up.save()
            return HttpResponseRedirect("/users/" + request.user.username)
        else:
            # invalid form
            print("Errors: " + form.errors)
    else:
        form = AddInterestsForm(request)
    return render_to_response(
        'add_interests.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))


@login_required
def remove_interests(request):
    if request.method == 'POST':
        form = RemoveInterestsForm(request, request.POST)
        print(form.errors)
        if form.is_valid():
            up = request.user.get_profile()
            # get all of form data and remove as applicable
            to_go_interests = form.cleaned_data['to_go_interests']
            for i in to_go_interests:
                up.other_tags.remove(r)
            up.save()
            return HttpResponseRedirect("/users/" + request.user.username)
        else:
            # invalid form
            print("Errors: " + form.errors)
    else:
        form = RemoveInterestsForm(request)
    return render_to_response(
        'remove_interests.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))



def contacts(request, username):

    h_user = get_object_or_404(Profile, name__iexact=username)
    return render_to_response(
            'contact_list.html',
            {
                'h_user':   h_user,
                'all_tags': Tag.objects.all()
            },
            RequestContext(request))


@login_required
def remove_contact(request, username, togo_friend):

    h_user = get_object_or_404(Profile, name__iexact=username)
    if h_user.name != request.user.username:
        return HttpResponseForbidden("Play with yer own black book!")
    old_friend = get_object_or_404(Profile, name__iexact=togo_friend)
    h_user.contacts.remove(old_friend)
    return HttpResponseRedirect('/users/' + username + '/contacts/')


@login_required
def add_contact(request, username, new_friend_name):

    if request.method == 'POST':
        h_user = get_object_or_404(Profile, name__iexact=username)
        if h_user.name != request.user.username:
            return HttpResponseForbidden("Play with yer own black book!")
        new_friend = get_object_or_404(Profile, name__iexact=new_friend_name)
        if username != new_friend_name:
            h_user.contacts.add(new_friend)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)

