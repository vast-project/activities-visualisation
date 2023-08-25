from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.db.models import Q
from .models import *

class ReadonlyFieldsAdmin(admin.ModelAdmin):
    ordering = ["name"]
    search_fields = ["name"]
    def get_readonly_fields(self, request, obj=None):
        fields = ()
        if obj:
            fields = ["created_by"]
            for f in ("qr_code", "uriref", "image_resource_id", "image_uriref", "image_preview", "document_resource_id", "document_uriref", "questionnaire_wp_form_id"):
                if getattr(obj, f, False):
                    fields.append(f)

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

    def get_list_filter(self, request):
        list_filter = []

        for field in self.get_fields(request):
            match field:
                case 'activity'|'activity_step'|'visitor_group'|'stimulus':
                    list_filter.append(f"{field}__name")
                case 'visitor':
                    list_filter.append(f"{field}__visitor_group__name")
        list_filter.append('created_by__username')
        return super().get_list_filter(request) + tuple(list_filter)

    def lookup_allowed(self, key, value):
        return True

    # Preselect the current user...
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['created_by'] = request.user.pk
        return initial

    class Media:
        css = {
             'all': ('css/admin_form_widgets.css',)
        }

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

class AutoCompleteObjectAdmin(FilterUserObjectsAdmin):
    def get_autocomplete_fields(self, request):
        fields = super().get_autocomplete_fields(request)
        return fields + ("object", )

    # Define a custom function to filter the autocomplete queryset
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Custom filtering logic (for example, search in Author's name)
        queryset |= self.model.objects.filter(Q(object__name__icontains=search_term))

        return queryset, use_distinct

class AutoCompleteSubjectObjectAdmin(FilterUserObjectsAdmin):
    def get_autocomplete_fields(self, request):
        fields = super().get_autocomplete_fields(request)
        return fields + ("subject", "object", )

    # Define a custom function to filter the autocomplete queryset
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Custom filtering logic (for example, search in Author's name)
        queryset |= self.model.objects.filter(Q(subject__name__icontains=search_term) | Q(object__name__icontains=search_term))

        return queryset, use_distinct

@admin.register(Stimulus)
class StimulusAdmin(FilterUserObjectsAdmin):
    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     match db_field.name:
    #         case 'questionnaire':
    #             kwargs['choices'] = Stimulus.get_questionnaires()
    #         case 'questionnaire_wp_post':
    #             kwargs['choices'] = Stimulus.get_wp_blog_posts()
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        match db_field.name:
            case 'questionnaire':
                return db_field.formfield(widget=forms.Select(choices = Stimulus.get_questionnaires()))
            case 'questionnaire_wp_post':
                return db_field.formfield(widget=forms.Select(choices = Stimulus.get_wp_blog_posts()))
        return super().formfield_for_dbfield(db_field, **kwargs)

    class Media:
       js = ["js/models/stimulus.js"]
Stimulus.set_fields_verbose_names()

for model in (Organisation, Class, Age,
              Activity, ActivityStep, Event, VisitorGroup, VisitorGroupQRCode,
              Visitor, Product, Concept, QuestionnaireEntry, QuestionnaireAnswer):
    admin.site.register(model, FilterUserObjectsAdmin)
    model.set_fields_verbose_names()

for model in (Language, Gender, Nature, Education, Nationality,
              OrganisationType, Context,
              ProductType, DigitisationApplication,
              ConceptType, Predicate, ):
    admin.site.register(model, ReadonlyFieldsAdmin)
    model.set_fields_verbose_names()

for model in (Statement, ):
    admin.site.register(model, AutoCompleteSubjectObjectAdmin)
    model.set_fields_verbose_names()

for model in (ProductStatement, ):
    admin.site.register(model, AutoCompleteObjectAdmin)
    model.set_fields_verbose_names()
