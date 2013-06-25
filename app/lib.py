# coding=UTF-8

from django.conf import settings

def context_processor(request):
    return {'CONTACT_EMAIL': settings.CONTACT_EMAIL}
