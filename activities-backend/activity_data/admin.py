from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from .models import *

class OrganisationTypeAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(OrganisationTypeAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(OrganisationTypeAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
     
class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields=('created_by',)
    def get_changeform_initial_data(self, request):
        get_data = super(OrganisationAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(OrganisationAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
       
class ClassAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ClassAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(ClassAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
      
class VisitorAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(VisitorAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(VisitorAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata

class VisitorGroupAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(VisitorGroupAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(VisitorGroupAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
       
class EventAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(EventAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
    
    def get_queryset(self, request): 
        alldata = super(EventAdmin, self).get_queryset(request)
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata.all()

class StimulusAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(StimulusAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(StimulusAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
      
class ProductAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ProductAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(ProductAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
      
class ContextAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ContextAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(ContextAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
 
class StatementAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(StatementAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(StatementAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
      
class LanguageAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(LanguageAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(LanguageAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
        
class AgeAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(AgeAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(AgeAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
      
class GenderAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(GenderAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(GenderAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata

class NatureAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(NatureAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(NatureAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata

class ActivityStepAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ActivityStepAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []
 
    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(ActivityStepAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
       
class ActivityAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ActivityAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_by"]
        else:
            return []

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        alldata = super(ActivityAdmin, self).get_queryset(request) 
        requsergroups = request.user.groups.all()
        if not request.user.is_superuser:
            qslist = []
            for group in requsergroups:
                users = User.objects.filter(groups__name=group)
                for user in users:
                    userdata=alldata.filter(created_by=user)
                    for dat in userdata:
                        qslist.append(dat.id)
            qslist = list(dict.fromkeys(qslist))
            return alldata.filter(pk__in=qslist)
        else:
            return alldata
          
admin.site.register(OrganisationType,OrganisationTypeAdmin)
admin.site.register(Organisation,OrganisationAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Visitor,VisitorAdmin)
admin.site.register(VisitorGroup,VisitorGroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Stimulus,StimulusAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Context,ContextAdmin)
admin.site.register(Statement,StatementAdmin)
admin.site.register(Language,LanguageAdmin)
admin.site.register(Age,AgeAdmin)
admin.site.register(Gender,GenderAdmin)
admin.site.register(Nature,NatureAdmin)
admin.site.register(ActivityStep,ActivityStepAdmin)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(VisitorGroupQRCode)
admin.site.register(Education)
admin.site.register(Nationality)
admin.site.register(ProductType)
admin.site.register(Predicate)
admin.site.register(Concept)
