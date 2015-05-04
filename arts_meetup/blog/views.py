from django.shortcuts               import get_object_or_404
from django.template                import loader, Context
from django.http                    import HttpResponse, HttpResponseRedirect
from django.template                import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils                   import simplejson

from arts_meetup.blog.models        import Post
from arts_meetup.users.models       import Profile

@login_required
def create(request):

    if request.method =='POST':
        body   = request.POST.get('body', '')

        if body:
            p = Post(author=request.user.get_profile(), body=body[:500])
            request.user.get_profile().save()
            p.save()
            if request.POST.get('type', '') == 'json':
                data = {'id': p.id}     # send id of created Post back in this
                return HttpResponse(
                        simplejson.dumps(data),
                        mimetype='application/json'
                    )
    return HttpResponseRedirect('/users/'+request.user.username+'/')


@login_required
def delete(request, id):
    print "Deleting id = " + id
    post = get_object_or_404(Post, id=id)
    if post.author == request.user.get_profile():
        post.delete()
        request.user.get_profile().save()
        return HttpResponseRedirect('/users/'+request.user.username+'/')
        return HttpResponse()
    else:
        return HttpResponseForbidden("Go clear out yer own things!")


def archive(request):

    posts = BlogPost.objects.all()
    t = loader.get_template("archive.html")
    c = Context({ 'posts': posts })
    print("Using the custom request context")
    return HttpResponse(t.render(c), context_instance=RequestContext(request, processors=[custom_proc]))


def custom_proc(request):

    print("Setting the custom request context")
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }
