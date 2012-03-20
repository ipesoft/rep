from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rep.views.home', name='home'),
    # url(r'^rep/', include('rep.foo.urls')),
    # Main page:
    url(r'^$', 'app.views.index'),
    url(r'^p/(?P<page_code>[-\w\d]+)/$', 'app.views.page'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

