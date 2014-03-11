from django.conf.urls.defaults import *
from django.contrib            import admin
from django.contrib.auth.views import login, logout


admin.autodiscover()

urlpatterns = patterns('',

    (r'^events/',           include('tridates.events.urls')),
    (r'^regions/',          include('tridates.regions.urls')),
    (r'^comments/',         include('django.contrib.comments.urls')),
    (r'^accounts/login',    login),
    (r'^accounts/logout',   logout),
    (r'^accounts/register', 'tridates.events.views.register'),
    (r'^$',                 'tridates.events.views.home'),
    
    # Admin
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^admin/', include(admin.site.urls)),
)
