import re

from django.http                    import *
from django.views.generic           import list_detail
from django.contrib.auth.decorators import login_required
from django.shortcuts               import render_to_response
from django.template                import RequestContext

from models                         import *
from forms                          import *
from arts_meetup.users.models       import Profile



def users_by_role(request, name):
    # Look up the role (and raise a 404 if it can't be found).
    try:
        role = RoleTag.objects.get(name__iexact=name)
    except RoleTag.DoesNotExist:
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_list(
        request,
        queryset = Profile.objects.filter(role=role),
        template_name = "tags/users_by_role.html",
        #template_object_name = "books",
        extra_context =
            {
                "role" :    role,
                'all_tags': Tag.objects.all()
            }
    )


def users_by_interest(request, name):
    # Look up the interest (and raise a 404 if it can't be found).
    try:
        interest = InterestTag.objects.get(name__iexact=name)
    except InterestTag.DoesNotExist:
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_list(
        request,
        queryset = Profile.objects.filter(interests=interest),
        template_name = "tags/users_by_interest.html",
        #template_object_name = "books",
        extra_context =
            {
                "interest" : interest,
                'all_tags': Tag.objects.all()
            }
    )



@login_required
def make_tag(request):
    no_more_tags = request.user.get_profile().role.all().count() >= Tag.MAX_TAGS
    if request.method == 'POST':
        form = MakeTagForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            tag_type     = 'R'              # hard coded while we don't use "OtherTag"
            tag_name_raw = cd['tag_name']
            tag_me       = cd['tag_me']
            name_parts   = re.compile('\\w+').findall(tag_name_raw)
            tag_name     = ''.join(name_parts).lower()

            if True:            # tag_type == 'R':
                rt = RoleTag.objects.get_or_create(name=tag_name)
                if tag_me and not no_more_tags:
                    request.user.get_profile().role.add(rt[0])
                    request.user.get_profile().save()
            elif tag_type == 'I':
                it = OtherTag.objects.objects.get_or_create(name=tag_name)
                if tag_me:
                    request.user.get_profile().interests.add(it[0])
            if tag_me:
                msg = "You've been tagged " + tag_name
            else:
                msg = "Made a tag '" + tag_name + "'"
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect("/users/" + request.user.username)
    else:
        form = MakeTagForm()
    return render_to_response(
            'maketag.html',
            {
                'form':         form,
                'no_more_tags': no_more_tags,
                'all_tags':     Tag.objects.all()
            },
            RequestContext(request)
        )
