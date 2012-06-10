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
    # Translation facility
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Static content page
    url(r'^p/(?P<page_code>[-\w\d]+)/$', 'app.views.show_page'),
    # Browse species
    url(r'^sp/?$', 'app.views.search_species'),
    # Species page
    url(r'^sp/(?P<species_id>\d+)/?$', 'app.views.show_species'),
    # Search page
    url(r'^sp/search/?$', 'app.views.search_page'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

