import re
import itertools
from operator                       import itemgetter

from django.forms.util              import ErrorList
from datetime                       import date
from django.db.models               import Q
from django.http                    import HttpResponseRedirect, HttpResponse
from django.shortcuts               import render_to_response
from django.contrib.auth.models     import User
from django.contrib                 import auth
from django.contrib.auth.decorators import login_required
from django.template                import RequestContext

from forms                          import *
from arts_meetup.users.models       import Profile
from arts_meetup.links.models       import URL
from arts_meetup.tags.models        import Tag


def render_to(template):

    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


def is_valid_date(uk_date):
    print "In is_valid_date and uk_date = " + uk_date
    print type(uk_date)
    print "Here we go!"
    valid = False
    try:
        sd  = re.compile('\\w+').findall(uk_date)
        sdn = map(int, sd)
        date(sdn[2], sdn[1], sdn[0])
        valid = True
    except:
        pass
    return valid


def register(request, acc_type):

    if request.user.is_authenticated():
        auth.logout(request)
    if request.method == 'POST':
        if acc_type == Profile.VENUE:
            form = VenueRegistrationForm(request.POST, request.FILES)
        elif acc_type == Profile.GROUP:
            form = GroupRegistrationForm(request.POST, request.FILES)
        else:
            form = IndividualRegistrationForm(request.POST, request.FILES)
        if form.is_valid():

            username            = form.cleaned_data['username']
            email               = form.cleaned_data['email']
            password1           = form.cleaned_data['password1']
            user                = User.objects.create_user(username, email, password1)
            user.save()

            profile             = Profile()
            profile.type        = acc_type
            profile.name        = username
            # profile.picture     = request.FILES['picture']
            profile.user        = user     # making foreign key to User object
            profile.city        = form.cleaned_data['city']
            profile.email_news  = form.cleaned_data['email_news']
            # tandcs              = form.cleaned_data['tandcs']
            if acc_type == Profile.VENUE or acc_type == Profile.GROUP:
                profile.org_name    = form.cleaned_data['name']
            else:
                profile.first_name  = form.cleaned_data['first_name']
                profile.last_name   = form.cleaned_data['last_name']
                profile.sex         = form.cleaned_data['sex']
                if is_valid_date(form.cleaned_data['dob']):
                    sd              = re.compile('\\w+').findall(form.cleaned_data['dob'])
                    profile.dob     = date(int(sd[0]), int(sd[1]), int(sd[2]))
            profile.save()

            user = auth.authenticate(username=username, password=password1)
            if user and user.is_active:
                auth.login(request, user)
                # return HttpResponseRedirect("/users/" + username)
                return HttpResponseRedirect("/users/add_roles/")
            else:
                return HttpResponseRedirect('/registration/disabledaccount')

        else :
            print(form.errors)

    if acc_type == Profile.VENUE:
        template = 'registration/register_venue.html'
        if request.method == 'GET': form = VenueRegistrationForm()
    elif acc_type == Profile.GROUP:
        template = 'registration/register_group.html'
        if request.method == 'GET': form = GroupRegistrationForm()
    else:
        template = 'registration/register_individual.html'
        if request.method == 'GET': form = IndividualRegistrationForm()
    return render_to_response(
        template,
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))



def login(request):

    # also need to test if user accepts cookies.
    # See "Setting Test Cookies" at djangobook.com
    if request.user.is_authenticated():
        print("Already authenticated")
        return render_to_response(
                'user_home.html',
                {
                    'all_tags': Tag.objects.all()
                },
                RequestContext(request))
    if request.method == 'POST':
        print("next = " + request.POST.get('next', ''))
        print("Post was made")
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            # get username and password and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                print("Yes, this is a user")
                if user.is_active:
                    print("... and an active one")
                    auth.login(request, user)
                    next_page = request.POST.get('next', '')
                    if not next_page:
                        next_page = "/users/" + request.user.username
                    print("Sending on to " + next_page)
                    return HttpResponseRedirect(next_page)
                else:
                    print("... but not active")
                    return HttpResponseRedirect('/registration/disabledaccount')
            else:
                form.errors['username'] = ErrorList(['Invalid username or password'])
        # Invalid login
        print("Bad login friend")
        return render_to_response(
                'registration/login.html',
                {'form': form, 'all_tags': Tag.objects.all()},
                RequestContext(request))
    else:
        print("GET call")
        form = LoginForm()
    print("Doing last resort")
    return render_to_response(
        'registration/login.html',
        {
            'form'             : form,
            'next'             : request.GET.get('next', ''),
            'all_tags'         : Tag.objects.all(),
            'updated_profiles' : Profile.objects.all().order_by('last_activity')[:10],
        },
        RequestContext(request))


def logout(request):
    print("Logging out %s", request.user.username)
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')
#        'registration/login.html',
#        {'form': form},
#        RequestContext(request))


def whoami(request):
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = 'nobody'
    return HttpResponse("User:  %s." % user)


def is_send_email(request):
    if request.user.is_authenticated():
        send = request.user.get_profile().email_msged
    else:
        send = '???'
    return HttpResponse("Should send?:  %s." % send)


@login_required
def change_password(request):
    print("Changing password")
    if request.method == 'POST':
        print("Post was made")
        form = ChangePasswordForm(request.POST)
        print(form.errors)
        # get username and password and login
        old_password  = form.cleaned_data['old_password']
        new_password1 = form.cleaned_data['new_password1']
        new_password2 = form.cleaned_data['new_password2']
        user = request.user
        if (user.check_password(old_password) and
                new_password1 == new_password2):
            print("trying to set new password to " + new_password1)
            user.set_password(new_password1)
            user.save()
            return HttpResponseRedirect('/users/' + request.user.username + '/')
    else:
        form = ChangePasswordForm()
    return render_to_response(
        'registration/change_password.html',
        {
            'form'      : form,
            'all_tags'  : Tag.objects.all()},
        RequestContext(request))


def mini_search(request):

    query = request.GET.get('q', '')
    if query:
        results = do_search(query)
    else:
        results = []
    results_friends_zip = []
    for r in results:
        if request.user.is_authenticated():
            f = r in request.user.get_profile().contacts.all()
        else:
            f = False
        results_friends_zip.append((r, f))
    return render_to_response("mini_search.html", {
            "zip":      results_friends_zip,
            "query":    query,
            'all_tags': Tag.objects.all(),
        }, RequestContext(request))



def flatten(li):
    if isinstance(li, Profile):  # and not li == '':
        return list([li])
    if len(li) == 0:
        return list()
    return flatten(li[0]) + flatten(li[1:])


def order(ul):
    s = {}
    for li in ul:
        if li in s:
            s[li] = s[li] + 1
        else:
            s[li] = 1
    slist = s.items()
    slist.sort(key=itemgetter(1), reverse=True)
    return map(lambda lis: lis[0], slist)

def icontains(ignore_terms, term):
    for ig in ignore_terms:
        if term.lower() == ig.lower():
            return True
    return False


def do_search(query):

    ignore_terms = ('the', 'of', 'and', 'or')

    terms = re.compile('[^\\s,;]+').findall(query)
    qs_results = []
    for term in terms:

        if term.find('@') > -1:
            # doing email search
            qs_results.append(
                Profile.objects.filter(user__email__iexact=term))
        elif not icontains(ignore_terms, term):
            # search on first / last name / org_name
            qs_results.append(Profile.objects.filter(first_name__iexact=term))
            qs_results.append(Profile.objects.filter(last_name__iexact=term))
            qs_results.append(Profile.objects.filter(org_name__icontains=term))

    iter_results = zip(itertools.chain(qs_results))
    iter_results = flatten(iter_results)
    return order(iter_results)


def send_home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/users/'+request.user.username+'/')
    else:
        return HttpResponseRedirect('/accounts/login/')
#        register(request)





# This is to work with
# http://localhost:8000/accounts/full_search/
# see also on dynamic forms:
# http://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
@render_to('full_search.html')
def full_search(request):

    do_search = request.GET.get('tag', '') and request.GET.get('start', '')
    if do_search:
        form = FullSearchForm(request)
        results = fun_search(request)
    else:
        results = []
        form = FullSearchForm(request)
    return {
        'form': form,
        'do_search': do_search,
        'no_menu_search': True,
        'results': results,
        }

# this is not the same as booking.views.uk_str_to_date
def uk_str_to_date(uk_date):
    split = uk_date.split('/')
    return split[2]+"-"+split[1]+"-"+split[0]


def valid_date(uk_date):
    valid = False
    try:
        d = (uk_str_to_date(uk_date)).split('-')
        datetime.date(int(d[0]), int(d[1]), int(d[2]))
        valid = True
    except:
        pass
    return valid


# I am going to hell for this method
def fun_search(request):

    role  = request.GET.get('tag', '')
    where = request.GET.get('where', '')
    s     = request.GET.get('start', '')
    e     = request.GET.get('until', '')

    if (not valid_date(str(s))) and (not valid_date(str(e))):
        if where:
            return User.objects.filter(
                    profile__city=where,
                    profile__role=role
                )
        else:
            return User.objects.filter(profile__role=role)
    if (not valid_date(str(s))) or (not valid_date(str(e))):
        return []
    s = uk_str_to_date(str(s))
    e = uk_str_to_date(str(e))

    bad_time = User.objects.filter(
            Q(profile__booking__start__lte=s,
                profile__booking__end__gte=s) |
            Q(profile__booking__start__lte=e,
                profile__booking__end__gte=e) |
            Q(profile__booking__start__gte=s,
                profile__booking__end__lte=e)
        ).distinct()

    right_place = User.objects.filter(
            profile__city=where,
            profile__role=role
        )

    available = []
    for r in right_place:
        try:
            bad_time.get(username=r.username)
        except User.DoesNotExist:
            available.append(r)

    return available

@login_required
def settings(request):

    acc_type = request.user.get_profile().type
    if request.method == 'POST':
        up = request.user.get_profile()

        if acc_type == Profile.VENUE:
            venue_form = VenueSettingsForm(request, request.POST)
            if venue_form.is_valid():
                up.org_name         = venue_form.cleaned_data['org_name']
                up.address_line_1   = venue_form.cleaned_data['address_line_1']
                up.address_line_2   = venue_form.cleaned_data['address_line_2']
                up.postcode         = venue_form.cleaned_data['postcode']
                up.telephone        = venue_form.cleaned_data['telephone']
                up.city             = venue_form.cleaned_data['city']
                request.user.email  = venue_form.cleaned_data['email']
                up.email_news       = venue_form.cleaned_data['email_news']
                up.email_msged      = venue_form.cleaned_data['email_msged']

        elif acc_type == Profile.GROUP:
            group_form = GroupSettingsForm(request, request.POST)
            if group_form.is_valid():
                up.org_name         = group_form.cleaned_data['org_name']
                up.address_line_1   = group_form.cleaned_data['address_line_1']
                up.address_line_2   = group_form.cleaned_data['address_line_2']
                up.postcode         = group_form.cleaned_data['postcode']
                up.telephone        = group_form.cleaned_data['telephone']
                up.city             = group_form.cleaned_data['city']
                request.user.email  = group_form.cleaned_data['email']
                up.email_news       = group_form.cleaned_data['email_news']
                up.email_msged      = group_form.cleaned_data['email_msged']

        else:
            person_form = PersonSettingsForm(request, request.POST)
            if person_form.is_valid():
                up.first_name       = person_form.cleaned_data['first_name']
                up.last_name        = person_form.cleaned_data['last_name']
                up.sex              = person_form.cleaned_data['sex']
                up.city             = person_form.cleaned_data['city']
                request.user.email  = person_form.cleaned_data['email']
                up.email_news       = person_form.cleaned_data['email_news']
                up.email_msged      = person_form.cleaned_data['email_msged']

        up.save()
        request.user.save()
        return HttpResponseRedirect("/users/" + request.user.username + "/")

    if Profile.VENUE == acc_type:
        if request.method == 'GET': form = VenueSettingsForm(request)
    elif Profile.GROUP == acc_type:
        if request.method == 'GET': form = GroupSettingsForm(request)
    else:
        if request.method == 'GET': form = PersonSettingsForm(request)
    return render_to_response(
            'settings.html',
            { 'form': form, 'all_tags': Tag.objects.all() },
            RequestContext(request)
        )


@login_required
def bio(request):
    if request.method == 'POST':
        form = BioForm(request, request.POST)
        if form.is_valid():
            bio = form.cleaned_data['bio']
            request.user.get_profile().bio = bio
            request.user.get_profile().save()
            return HttpResponseRedirect(
                    '/users/' + request.user.get_profile().name + '/'
                )
    else:
        form = BioForm(request)
    return render_to_response(
        'biography.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))


@login_required
def change_image(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.get_profile().picture = request.FILES['picture']
            request.user.get_profile().save()
            return HttpResponseRedirect(
                    '/users/' + request.user.get_profile().name + '/'
                )
    else:
        form = PictureForm()
    return render_to_response(
        'change_picture.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))
