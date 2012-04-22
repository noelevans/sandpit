from django.conf.urls.defaults        import patterns, include, url
from django.views.generic.list_detail import object_list
from django.contrib                   import admin

from poolratings.ratings.models       import Rating, Pool
from poolratings.ratings.views        import create_rating, pool_detail


admin.autodiscover()
pools = {
    'queryset'   :Pool.objects.all(),
    'allow_empty':True,
    'paginate_by':20,
}

urlpatterns = patterns('',
    # url(r'^$', 'poolratings.views.home', name='home'),
    # url(r'^poolratings/', include('poolratings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^pools/$',                                 object_list, pools),
    (r'^pool/(?P<pool_name>[\w|\W]+)/$',          pool_detail),
    (r'^rating/create/(?P<pool_name>[\w|\W]+)/$', create_rating),
)
