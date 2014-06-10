from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'

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
    # "Static" pages
    url(r'^about/?$', 'app.views.about'),
    url(r'^methods/?$', 'app.views.methods'),
    url(r'^ethno/overview/?$', 'app.views.ethno_overview'),
    url(r'^ethno/?$', 'app.views.ethno_overview'),
    url(r'^ethno/results/?$', 'app.views.ethno_results'),
    url(r'^hist/overview/?$', 'app.views.hist_overview'),
    url(r'^hist/?$', 'app.views.hist_overview'),
    url(r'^hist/results/?$', 'app.views.hist_results'),
    url(r'^hist/interview/(?P<interview_id>\d+)/?$', 'app.views.interview'),
    url(r'^faq/?$', 'app.views.faq'),
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PDF_ROOT,}),
    # web service
    url(r'^ws/1.0/info$', 'app.views.ws_info'),
    # Help content
    url(r'^help/(?P<content_id>[-\w\d]+)/?$', 'app.views.show_help'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)

wspatterns = i18n_patterns('',
    # web service
    url(r'^ws/1.0/?$', 'app.views.ws_metadata'),
    url(r'^ws/1.0/sp/?$', 'app.views.search_species', {'ws': True,}),
    url(r'^ws/1.0/sp/(?P<species_id>\d+)/?$', 'app.views.show_species', {'ws': True,}),
)

urlpatterns += wspatterns

try:
    import my_urls
    urlpatterns += patterns('', url(r'^', include('my_urls')), )
except:
    pass
