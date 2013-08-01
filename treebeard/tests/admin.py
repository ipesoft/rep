import datetime

from django.contrib import admin
from treebeard.admin import admin_factory
from treebeard.forms import movenodeform_factory

from treebeard.tests.models import BASE_MODELS

for model in BASE_MODELS:
    form_class = movenodeform_factory(model)
    admin_class = admin_factory(form_class)
    admin.site.register(model, admin_class)
