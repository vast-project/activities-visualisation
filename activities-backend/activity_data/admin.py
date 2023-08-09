from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from .models import *

class ReadonlyFieldsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        fields = ()
        if obj:
            fields = ["created_by"]
            if getattr(obj, "qr_code", False):
                fields.append("qr_code")
            if getattr(obj, "uriref", False):
                fields.append("uriref")
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        
        # Rearrange the fields to have 'name' as the first field
        for section_name, section_options in fieldsets:
            if 'name' in section_options['fields']:
                section_options['fields'] = ('name',) + tuple(
                    field for field in section_options['fields'] if field != 'name'
                )
                break
        
        return fieldsets

    # Preselect the current user...
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['created_by'] = request.user.pk
        return initial

class FilterUserObjectsAdmin(ReadonlyFieldsAdmin):

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
              Visitor, Product, Concept, Statement,):
    admin.site.register(model, FilterUserObjectsAdmin)

for model in (Language, Gender, Nature, Education, Nationality,
              OrganisationType, Context, 
              ProductType, DigitisationApplication,
              Predicate, ):
    admin.site.register(model, ReadonlyFieldsAdmin)
