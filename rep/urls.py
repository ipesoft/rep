from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from django.contrib import admin

from app import views

handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'

urlpatterns = [
    # Main page:
    url(r'^$', views.index),
    # Translation facility
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Static content page
    url(r'^p/(?P<page_code>[-\w\d]+)/$', views.show_page),
    # Browse species
    url(r'^sp/?$', views.search_species),
    # Species page
    url(r'^sp/(?P<species_id>\d+)/?$', views.show_species),
    # "Static" pages
    url(r'^about/?$', views.about),
    url(r'^methods/?$', views.methods),
    url(r'^ethno/overview/?$', views.ethno_overview),
    url(r'^ethno/?$', views.ethno_overview),
    url(r'^ethno/results/?$', views.ethno_results),
    url(r'^hist/overview/?$', views.hist_overview),
    url(r'^hist/?$', views.hist_overview),
    url(r'^hist/results/?$', views.hist_results),
    url(r'^hist/interview/(?P<interview_id>\d+)/?$', views.interview),
    url(r'^faq/?$', views.faq),
    #url(r'^docs/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.PDF_ROOT,}),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # web service
    url(r'^ws/1.0/info$', views.ws_info),
    # Help content
    url(r'^help/(?P<content_id>[-\w\d]+)/?$', views.show_help),

    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
]

wspatterns = i18n_patterns('',
    # web service
    url(r'^ws/1.0/?$', views.ws_metadata),
    url(r'^ws/1.0/sp/?$', views.search_species, {'ws': True,}),
    url(r'^ws/1.0/sp/(?P<species_id>\d+)/?$', views.show_species, {'ws': True,}),
)

urlpatterns += wspatterns

try:
    import my_urls
    urlpatterns += myurlpatterns
except:
    pass

if settings.DEBUG:
    urlpatterns += static('docs/', document_root=settings.PDF_ROOT)
