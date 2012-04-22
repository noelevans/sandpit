from django.shortcuts                   import get_object_or_404
from django.views.generic.create_update import get_model_and_form_class
from django.views.generic.create_update import create_object
from django.http                        import HttpResponseRedirect
from django.shortcuts                   import render_to_response
from django.core.context_processors     import csrf
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_detail

from ratings.models                     import Pool, Rating, RatingForm


def create_rating(request, pool_name):
    pool = get_object_or_404(Pool, name=pool_name)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        form.pool    = pool
        #form.creator = 
        if form.is_valid():
            rating = form.save(commit=False)
            rating.pool = pool
            rating.save()
            return HttpResponseRedirect('/pool/%s' % pool_name)
    else:
        form = RatingForm(initial={'pool':pool})
    c = {'form': form}
    return render_to_response(
            'ratings/rating_form.html', 
            c, 
            context_instance=RequestContext(request)
        )

def pool_detail(request, pool_name):
    pool = get_object_or_404(Pool, name=pool_name)
    return object_detail(
        request,
        queryset = Pool.objects.all(),
        object_id = pool.id,
        extra_context={'pool_name':pool_name}
    )
