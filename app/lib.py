# coding=UTF-8

from django.conf import settings

def context_processor(request):
    return {'CONTACT_LINK': settings.CONTACT_LINK}
