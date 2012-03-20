from django.conf import settings
from app.models import Page
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
    c = RequestContext(request, {'IPE_URL': settings.IPE_URL})
    return render_to_response( 'index.html', c )

def page(request, page_code):
    pages = Page.objects.filter(code=page_code)
    if len(pages) == 0:
        raise Http404
    try:
        p = pages.get(lang=settings.LANGUAGE_CODE)
    except Page.DoesNotExist:
        # Get first
        p = pages[0]
    
    c = RequestContext(request, {'page': p, 'IPE_URL': settings.IPE_URL})
    
    return render_to_response( 'page.html', c )
