from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.apps import apps
# https://djangopackages.org/grids/g/model-ordering/
# https://github.com/django-ordered-model/django-ordered-model
# https://django-admin-sortable2.readthedocs.io/en/latest/
from adminsortable2.admin import SortableAdminMixin, SortableAdminBase, SortableStackedInline
from .models import *
from itertools import chain

if apps.is_installed("unfold"):
    from unfold.admin import ModelAdmin
else:
    ModelAdmin = admin.ModelAdmin

admin.site.site_header = _('Model Admin')
admin.site.site_title  = _('VAST Model Admin')

class ShowNameActivityMixin:
    list_display = ["name", "activity"]
    ordering = ["activity", "name"]
    search_fields = ["name", "activity__name"]
    #list_display_links = ["activity"]

#class ReadonlyFieldsAdmin(admin.ModelAdmin):
class ReadonlyFieldsAdmin(ModelAdmin):
    list_display = ["name",]
    ordering = ["name"]
    search_fields = ["name"]
    def get_readonly_fields(self, request, obj=None):
        fields = ()
        if obj:
            if request.user.is_superuser:
                fields = []
            else:
                fields = ["created_by"]
            ro_fields = ("qr_code", "image_resource_id", "image_uriref", "image_preview", "document_resource_id", "document_uriref", "questionnaire_wp_form_id", "get_repository_url")
            if not isinstance(obj, DigitisationApplication):
                ro_fields += ("uriref",)
            for f in ro_fields:
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

    # Make sure delete() is called on deleted objects!
    def delete_queryset(self, request, queryset):
        # Perform custom delete logic here
        for obj in queryset:
            obj.delete()
        self.message_user(request, f"{queryset.count()} objects were deleted.")

    # Define a custom action to store all objects in the RDF store...
    def custom_store_action(self, request, queryset):
        rdf = RDFStoreVAST()
        for obj in queryset:
            rdf.save(type(obj).__name__, obj, commit=False)
        rdf.commit()
        del rdf
        self.message_user(request, f"{queryset.count()} objects were saved in the RDF store.")
    custom_store_action.short_description = "Save selected objects (in the RDF store)"

    # Override the default delete action to use the custom action
    actions = [custom_store_action]

    class Media:
        css = {
             'all': ('css/admin_form_widgets.css',)
        }

class FilterUserObjectsAdmin(ReadonlyFieldsAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # group_users = {request.user, }
        # for group in request.user.groups.all():
        #     group_users.update(User.objects.filter(groups__id=group.pk))
        group_users = self.model.get_group_users(request.user)
        return qs.filter(created_by__in=group_users)

        # For Django < 1.6, override queryset instead of get_queryset
        # alldata = super(OrganisationTypeAdmin, self).get_queryset(request)
        # alldata = super().get_queryset(request)
        # requsergroups = request.user.groups.all()
        # qslist = []
        # for group in requsergroups:
        #     users = User.objects.filter(groups__name=group)
        #     for user in users:
        #         userdata=alldata.filter(created_by=user)
        #         for dat in userdata:
        #             qslist.append(dat.id)
        # qslist = list(dict.fromkeys(qslist))
        # return alldata.filter(pk__in=qslist)

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

class AutoCompleteValueAdmin(FilterUserObjectsAdmin):
    def get_autocomplete_fields(self, request):
        fields = super().get_autocomplete_fields(request)
        return fields + ("value", )

    # Define a custom function to filter the autocomplete queryset
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Custom filtering logic (for example, search in Author's name)
        queryset |= self.model.objects.filter(Q(value__name__icontains=search_term))

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

## Expose two interfaces to Visitor: Visitor & VirtualVisitor
@admin.register(Visitor)
class VisitorAdmin(ShowNameActivityMixin, FilterUserObjectsAdmin):
    exclude = ('visitor_type', 'visitors_number', 'visitors')
    #def get_queryset(self, request):
    #    queryset = super().get_queryset(request)
    #    return queryset.filter(visitor_type='real')
Visitor.set_fields_verbose_names()
class VirtualVisitorAdminForm(forms.ModelForm):
    class Meta:
        model = VirtualVisitor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['visitor_type'].initial = 'group'
@admin.register(VirtualVisitor)
class VirtualVisitorAdmin(FilterUserObjectsAdmin):
    form = VirtualVisitorAdminForm
VirtualVisitor.set_fields_verbose_names()

##
## Activity Inline Steps...
##
#class ActivityStepsInline(admin.StackedInline):
class ActivityStepsInline(SortableStackedInline):
    model = ActivityStep
    extra = 0
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "description", "stimulus", "step_order"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["name_local", "description_local", "language_local"],
            },
        ),
    ]

@admin.register(Activity)
class ActivityAdmin(SortableAdminBase, FilterUserObjectsAdmin):
    inlines = [
        ActivityStepsInline,
    ]
Activity.set_fields_verbose_names()

for model in (Organisation, Class, Age,
              VisitorGroup, VisitorGroupQRCode,
              Product,
              QuestionnaireEntry, QuestionnaireQuestion, QuestionnaireAnswer):
    admin.site.register(model, FilterUserObjectsAdmin)
    model.set_fields_verbose_names()

class FilterUserObjectsShowActivityAdmin(ShowNameActivityMixin, FilterUserObjectsAdmin):
    pass

for model in (Event, ):
    admin.site.register(model, FilterUserObjectsShowActivityAdmin)
    model.set_fields_verbose_names()

class ActivityStepAdmin(FilterUserObjectsAdmin):
    list_display = ["name", "step_order", "activity"]
    ordering     = ["activity", "step_order", "name"]
    search_fields = ["name", "activity__name"]

for model in (ActivityStep, ):
    admin.site.register(model, ActivityStepAdmin)
    model.set_fields_verbose_names()

for model in (Language, Gender, Nature, Education, Nationality,
              OrganisationType, Context,
              ProductType, DigitisationApplication,
              Concept, ConceptType, Predicate,
              CulturalHeritageArtifact, EuropeanaCulturalHeritageArtifact):
    admin.site.register(model, ReadonlyFieldsAdmin)
    model.set_fields_verbose_names()

for model in (Statement, ):
    admin.site.register(model, AutoCompleteSubjectObjectAdmin)
    model.set_fields_verbose_names()

for model in (ProductStatement, ):
    admin.site.register(model, AutoCompleteObjectAdmin)
    model.set_fields_verbose_names()

for model in (ProductAnnotation, ):
    admin.site.register(model, AutoCompleteValueAdmin)
    model.set_fields_verbose_names()

