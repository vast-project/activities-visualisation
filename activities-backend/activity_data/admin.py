from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from .models import *

class ReadonlyFieldsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by", "qr_code", "uriref"]
        else:
            return []

class FilterUserObjectsAdmin(ReadonlyFieldsAdmin):
    # Preselect the current user...
    def get_changeform_initial_data(self, request):
        # get_data = super(OrganisationTypeAdmin, self).get_changeform_initial_data(request)
        get_data = super().get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_queryset(self, request): 
        if request.user.is_superuser:
            return super().get_queryset(request)

        # For Django < 1.6, override queryset instead of get_queryset
        # alldata = super(OrganisationTypeAdmin, self).get_queryset(request) 
        alldata = super().get_queryset(request) 
        requsergroups = request.user.groups.all()
        qslist = []
        for group in requsergroups:
            users = User.objects.filter(groups__name=group)
            for user in users:
                userdata=alldata.filter(created_by=user)
                for dat in userdata:
                    qslist.append(dat.id)
        qslist = list(dict.fromkeys(qslist))
        return alldata.filter(pk__in=qslist)


for model in (Organisation, Class, Age, 
              Activity, Stimulus, ActivityStep, Event, VisitorGroup, VisitorGroupQRCode,
              Visitor, Product, Statement,):
    admin.site.register(model, FilterUserObjectsAdmin)

for model in (Language, Gender, Nature, Education, Nationality,
              OrganisationType, Context, 
              ProductType, Concept, DigitisationApplication,):
    admin.site.register(model, ReadonlyFieldsAdmin)
