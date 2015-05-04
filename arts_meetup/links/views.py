from django.shortcuts               import get_object_or_404
from django.http                    import *
from django.shortcuts               import render_to_response
from django.contrib.auth.decorators import login_required
from django.template                import RequestContext

from models                         import URL
from forms                          import AddUserLinkForm
from arts_meetup.users.models       import Profile
from arts_meetup.tags.models        import Tag



def user_links(request, username):
    h_user = get_object_or_404(Profile, name__iexact=username)
    return render_to_response(
            'user_links.html',
            {
                'h_user':   h_user,
                'my_links': URL.objects.filter(user=h_user),
                'all_tags': Tag.objects.all()
            },
            RequestContext(request)
        )


@login_required
def add(request):
    if request.method == 'POST':
        form = AddUserLinkForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['link'].startswith('http://'):
                form.cleaned_data['link'] = 'http://' + form.cleaned_data['link']
        if form.is_valid():
            cd = form.cleaned_data
            url                = URL()
            url.name           = cd['label']
            url.other_profile  = cd['link']
            url.user           = request.user.get_profile()
            url.type           = URL.PERFORMANCES
            url.save()
            request.user.get_profile().save()
            return HttpResponseRedirect(
                    '/links/' + request.user.get_profile().name + '/'
                )
    else:
        form = AddUserLinkForm()
    return render_to_response(
        'add_user_link.html',
        {
            'form':     form,
            'all_tags': Tag.objects.all()
        },
        RequestContext(request))



@login_required
def delete(request, id):
    link = get_object_or_404(URL, id=id)
    if link.user == request.user.get_profile():
        link.delete()
        return HttpResponseRedirect(
                '/links/' + request.user.get_profile().name + '/'
            )
    return HttpResponseForbidden("Manager yer own links!")
