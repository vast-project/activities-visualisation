from django.core.files.storage import FileSystemStorage
from django.forms import Form, ModelForm, DateTimeInput, SplitDateTimeWidget
from django.forms.models import inlineformset_factory, modelformset_factory
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime, RelatedFieldWidgetWrapper
from django.contrib import admin
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineRadios, AccordionGroup, Accordion
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Button, Submit, Row, Column, TEMPLATE_PACK
from .custom_layout_object import *
from activity_data.models import *
from activity_data.admin import *
from markdown import markdown
import re
import copy
import os

def formfield_for_dbfield(db_field, **kwargs):
    match db_field.name:
        case "date" | "date_from" | "date_to" | "date_of_visit":
            # Change the form field for dates to a SplitDateTimeField
            return forms.SplitDateTimeField(**kwargs)

    formfield = db_field.formfield(**kwargs)
    # ForeignKey or ManyToManyFields
    if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
        wrapper_kwargs = {
            'can_add_related':    True,
            'can_change_related': True,
            'can_delete_related': True,
            'can_view_related':   True,
        }
        formfield.widget = RelatedFieldWidgetWrapper(
            formfield.widget,
            db_field.remote_field,
            admin.site,
            **wrapper_kwargs,
        )
    return formfield

class CrispyForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class        = 'form-horizontal'
        self.helper.label_class       = 'col-lg-2'
        self.helper.field_class       = 'col-lg-8'
        self.helper.form_method       = 'post'
        self.helper.form_tag          = False
        self.helper.disable_csrf      = True
        self.helper.include_media     = False
        layout = self.initLayout()
        if layout:
            self.helper.layout = layout
        header = self.header()
        if header:
            self.helper.layout.insert(0, HTML(markdown(header)))
        self.adjustLayout()

    def classInline(self):
        self.helper.template = f'{TEMPLATE_PACK}/table_inline_formset.html'
        self.helper.form_class        = ''
        self.helper.label_class       = ''
        self.helper.field_class       = ''

    def getAdminURL(self, text, model, action='changelist', args=[]):
        return f'<a href="{{% url \'admin:activity_data_{model}_{action}\' {" ".join([str(x) for x in args])} %}}" target="_blank">{text}</a>'

    def headerMarkdown(self):
        return None

    def headerTableMarkdown(self):
        return ""

    def headerTable(self, objects=None, model='activity'):
        if not objects:
            return None
        html = self.headerTableMarkdown()
        html += '''\n<table class="fixed_header">
 <thead>
   <tr>
     <th>Name</th><th>User</th><th>Actions</th>
   </tr>
 </thead>
 <tbody>\n'''
        for obj in objects:
            html += f"  <tr><td>{obj.name}</td><td>{obj.created_by.username} (id={obj.created_by.pk})</td>"
            html += f"<td>{self.getAdminURL('edit', model, 'change', [obj.pk])}, "
            html += f"{self.getAdminURL('delete', model, 'delete', [obj.pk])}</td>"
            html += "</tr>\n"
        html += "</tbody></table>"
        return html

    def headerTableObjects(self):
        return None

    def modelName(self):
        return None

    def header(self):
        result = None
        m = self.headerMarkdown()
        t = self.headerTable(self.headerTableObjects(), self.modelName())
        if m:
            result = m
        if t:
            if result:
                result += t
            else:
                result = t
        return result

    def initLayout(self):
        return None

    def adjustLayout(self):
        pass

    def all_other_fields(self, manually_rendered_fields=None):
        model = getattr(self, 'model', None)
        if not model:
            return Layout()
        if not manually_rendered_fields:
            manually_rendered_fields = self.manually_rendered_fields
        all_other_fields = [f.name for f in self.model._meta.get_fields() if f not in manually_rendered_fields]
        return Layout(*all_other_fields)

    class Media:
        js = [
            "admin/js/vendor/jquery/jquery.min.js",
            "admin/js/jquery.init.js",
            "admin/js/core.js",
            "admin/js/admin/RelatedObjectLookups.js",
            "admin/js/actions.js",
            "admin/js/urlify.js",
            "admin/js/prepopulate.js",
            "admin/js/vendor/xregexp/xregexp.min.js",
        ]
        css = {"all": ("css/form_widgets.css", "admin/css/forms.css",)}

class VASTForm(ModelForm, CrispyForm):

    def headerMarkdown(self):
        return "# Create a new %s ({{ wizard.steps.step1 }}/{{ wizard.steps.count }})" % getattr(self._meta.model, 'verbose_name', str(self._meta.model.__name__))

    class Meta:
        exclude = ('uuid', 'created', 'updated', 'name_md5', '_id', 'id', 'qr_code', 'uriref', 'image_uriref')
        widgets = {
            # Important: If more fields are added here for AdminSplitDateTime(),
            # function formfield_for_dbfield() must be also updated.
            "date":          AdminSplitDateTime(),
            "date_from":     AdminSplitDateTime(),
            "date_to":       AdminSplitDateTime(),
            "date_of_visit": AdminSplitDateTime(),
            "created_by":    forms.HiddenInput(),
        }
        formfield_callback = formfield_for_dbfield
        field_order = ('name',)

    # class Media:
    #     js = [
    #         "admin/js/vendor/jquery/jquery.min.js",
    #         "admin/js/jquery.init.js",
    #         "admin/js/core.js",
    #         "admin/js/admin/RelatedObjectLookups.js",
    #         "admin/js/actions.js",
    #         "admin/js/urlify.js",
    #         "admin/js/prepopulate.js",
    #         "admin/js/vendor/xregexp/xregexp.min.js",
    #     ]
    #     css = {"all": ("admin/css/forms.css",)}

class ActivityStepForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = ActivityStep

    def adjustLayout(self):
        self.classInline()

    def headerMarkdown(self):
        return None
        return """{% load static %}
# Activity Steps Model
An activity must have one or more **Activity Steps**. An activity step must contain a single stimulus.

In this step, please select a **Stimulus** at the form end (or add a new stimulus using the green plus button
![Add]({% static 'admin/img/icon-addlink.svg' %}), and finally provide a name for the activity step.
The name must be unique.

(Fields marked with * are required.)
"""

class ActivityStepFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))
        self.form_method       = 'post'
        self.form_tag          = False
        self.disable_csrf      = True
        self.include_media     = False
        self.template          = f'{TEMPLATE_PACK}/table_inline_formset.html'
        self.all().wrap_together(Div, css_class=f'formset_row-{self.formtag_prefix}')

ActivityStepFormSet = inlineformset_factory(
    Activity,
    ActivityStep,
    form=ActivityStepForm,
    exclude=('id',),
    #exclude=('activity',),
    extra=0,            # number of extra empty forms to display
    min_num=1,          # number of minimum filled forms
    can_delete=False,   # show a checkbox in each form to delete the row
    # formfield_callback = formfield_for_dbfield,
    # widgets = {
    #     "created_by": forms.HiddenInput(),
    # }
)

# https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
class ActivityForm(VASTForm):
    activity_steps = ActivityStepFormSet()
    def __init__(self, *args, **kwargs):
        formset_kwargs = copy.deepcopy(kwargs)
        # Get prefix
        prefix = kwargs.get('prefix')
        # Get number of forms
        data   = kwargs.get('data')
        if data:
            total_forms = int(data.get(f'{prefix}-TOTAL_FORMS')[0])
            # Set created_by...
            for key in kwargs.get('initial').keys():
                value = formset_kwargs['data'][f'{prefix}-0-{key}']
                for i in range(1, total_forms):
                    formset_kwargs['data'][f'{prefix}-{i}-{key}'] = value
        else:
            total_forms = 1
        # Give as many initial objects as forms...
        formset_kwargs['initial'] = [kwargs.get('initial')] * (total_forms)
        # TODO: Handle instances
        formset_kwargs.pop('instance')
        self.activity_steps = ActivityStepFormSet(*args, **formset_kwargs)
        super().__init__(*args, **kwargs)

    class Meta(VASTForm.Meta):
        model = Activity
    # class AdminForm:
    #     admin_form_class = ActivityAdmin

    def full_clean(self):
        super().full_clean()
        self.activity_steps.full_clean()

    # def clean(self):
    #     data = super().clean()
    #     print("CLEAN:", data, flush=True)
    #     self.activity_steps.full_clean()
    #     print("CLEAN2:", self.activity_steps.clean())
    #     return data

    def is_valid(self):
        is_valid = super().is_valid()
        print("IS VALID 1:", is_valid, self.errors)
        if not is_valid:
            return is_valid
        is_valid = self.activity_steps.is_valid()
        print("IS VALID 2:", is_valid, self.activity_steps.errors)
        return is_valid

    def save(self, commit=True):
        #print("save:", commit)
        if commit:
            instance = super().save(commit)
            instances = self.activity_steps.save(False)
            for obj in instances:
                obj.activity = instance
                obj.save(commit)
        else:
            instance = super().save(commit)
            instances = self.activity_steps.save(commit)
            #print("Activity:", instance)
            #print("Steps:", instances)
        return instance, ( ('activity',), instances)

    def save_m2m():
        super().save_m2m()
        self.activity_steps.save_m2m()

    def adjustLayout(self):
        self.helper.layout.append(
            Div(
                Fieldset('Add Activity Steps',
                    HTML(markdown("""{% load static %}
An activity must have one or more **Activity Steps**. An activity step must contain a single stimulus.

In this step, please select a **Stimulus** at the form right end (or add a new stimulus using the green plus button
![Add]({% static 'admin/img/icon-addlink.svg' %})), and finally provide a name for the activity step.
The name must be unique. (Fields marked with * are required.)
""")),
                    Div(
                        Formset('activity_steps'),
                        css_class="activity_steps_form"
                    ),
                ),
                css_class='embedded_formset'
            )
        )

class EventForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = Event

class VisitorGroupForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = VisitorGroup

class VisitorGroupQRCodeForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = VisitorGroupQRCode

class VisitorForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = Visitor

class ProductForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = Product
        exclude = ('uuid', 'created', 'updated', 'name_md5', '_id', 'id', 'qr_code', 'uriref',
                   'name', 'description', 'name_local', 'description_local', 'language_local', 'image_resource_id', 'image_uriref', 'document_resource_id', 'document_uriref')

##
## Product Statements form: A form for adding statements into an existing product.
##

class StatementForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = Statement
        exclude = ('uuid', 'created', 'updated', 'name_md5', '_id', 'id', 'qr_code', 'uriref',
                   'name', 'description', 'name_local', 'description_local', 'language_local',)

    def adjustLayout(self):
        self.classInline()

StatementFormSet = inlineformset_factory(
    Product,
    Statement,
    fields=('subject', 'predicate', 'object'),
    form=StatementForm,
    #formset=StatementForm,
    exclude=('id',),
    #exclude=('activity',),
    extra=0,            # number of extra empty forms to display
    min_num=1,          # number of minimum filled forms
    can_delete=False,   # show a checkbox in each form to delete the row
)

class ProductStatementsForm(CrispyForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        # widget=RelatedFieldWidgetWrapper(
        #     forms.Select, 
        #     queryset=Product.objects.all(),
        #     related_url='admin:activity_data_product_changelist',
        # ),
    )
    statements = StatementFormSet()
    def __init__(self, *args, **kwargs):
        formset_kwargs = copy.deepcopy(kwargs)
        # Get prefix
        prefix = kwargs.get('prefix')
        # Get number of forms
        data   = kwargs.get('data')
        if data:
            total_forms = int(data.get(f'{prefix}-TOTAL_FORMS')[0])
            # Set initial...
            for key in kwargs.get('initial').keys():
                value = formset_kwargs['data'][f'{prefix}-0-{key}']
                for i in range(1, total_forms):
                    formset_kwargs['data'][f'{prefix}-{i}-{key}'] = value
        else:
            total_forms = 1
        # Give as many initial objects as forms...
        formset_kwargs['initial'] = [kwargs.get('initial')] * (total_forms)
        # TODO: Handle instances
        #formset_kwargs.pop('instance')
        self.statements = StatementFormSet(*args, **formset_kwargs)
        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
        self.statements.full_clean()

    def is_valid(self):
        is_valid = super().is_valid()
        print("IS VALID 1:", is_valid, self.errors)
        if not is_valid:
            return is_valid
        is_valid = self.statements.is_valid()
        print("IS VALID 2:", is_valid, self.statements.errors)
        return is_valid

    def save(self, commit=True):
        #print("save:", commit)
        if commit:
            instance = super().save(commit)
            instances = self.statements.save(False)
            for obj in instances:
                obj.product = instance
                obj.save(commit)
        else:
            instance = super().save(commit)
            instances = self.statements.save(commit)
        return instance, ( ('statements',), instances)

    def save_m2m():
        super().save_m2m()
        self.statements.save_m2m()

    def adjustLayout(self):
        self.helper.layout.append(
            Div(
                Fieldset('Add Statements',
                    HTML(markdown("""{% load static %}
A statement associates a subject (i.e. value, concept, etc.) to an object (i.e. another value) through a predicate (a relation name).
An Product must have one or more **Statements**. (Fields marked with * are required.)
""")),
                    Div(
                        Formset('statements'),
                        css_class="statements_form"
                    ),
                ),
                css_class='embedded_formset'
            )
        )

class ProductStatementForm(VASTForm):
    class Meta(VASTForm.Meta):
        model = ProductStatement
        exclude = ('uuid', 'created', 'updated', 'name_md5', '_id', 'id', 'qr_code', 'uriref',
                   'name', 'description', 'name_local', 'description_local', 'language_local',)

    def adjustLayout(self):
        self.classInline()

ProductStatementFormSet = inlineformset_factory(
    Product,
    ProductStatement,
    fields=('predicate', 'object'),
    form=ProductStatementForm,
    exclude=('id',),
    extra=0,            # number of extra empty forms to display
    min_num=1,          # number of minimum filled forms
    can_delete=False,   # show a checkbox in each form to delete the row
)

class ProductProductStatementsForm(CrispyForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        # widget=RelatedFieldWidgetWrapper(
        #     forms.Select, 
        #     queryset=Product.objects.all(),
        #     related_url='admin:activity_data_product_changelist',
        # ),
    )
    statements = ProductStatementFormSet()
    def __init__(self, *args, **kwargs):
        formset_kwargs = copy.deepcopy(kwargs)
        # Get prefix
        prefix = kwargs.get('prefix')
        # Get number of forms
        data   = kwargs.get('data')
        if data:
            total_forms = int(data.get(f'{prefix}-TOTAL_FORMS')[0])
            # Set initial...
            for key in kwargs.get('initial').keys():
                value = formset_kwargs['data'][f'{prefix}-0-{key}']
                for i in range(1, total_forms):
                    formset_kwargs['data'][f'{prefix}-{i}-{key}'] = value
        else:
            total_forms = 1
        # Give as many initial objects as forms...
        formset_kwargs['initial'] = [kwargs.get('initial')] * (total_forms)
        # TODO: Handle instances
        #formset_kwargs.pop('instance')
        self.statements = ProductStatementFormSet(*args, **formset_kwargs)
        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
        self.statements.full_clean()

    def is_valid(self):
        is_valid = super().is_valid()
        print("IS VALID 1:", is_valid, self.errors)
        if not is_valid:
            return is_valid
        is_valid = self.statements.is_valid()
        print("IS VALID 2:", is_valid, self.statements.errors)
        return is_valid

    def save(self, commit=True):
        #print("save:", commit)
        if commit:
            instance = super().save(commit)
            instances = self.statements.save(False)
            for obj in instances:
                obj.subject = instance
                obj.save(commit)
        else:
            instance = super().save(commit)
            instances = self.statements.save(commit)
        return instance, ( ('statements',), instances)

    def save_m2m():
        super().save_m2m()
        self.statements.save_m2m()

    def adjustLayout(self):
        self.helper.layout.append(
            Div(
                Fieldset('Add Product Statements',
                    HTML(markdown("""{% load static %}
A statement associates a subject (i.e. value, concept, etc.) to an object (i.e. another value) through a predicate (a relation name).
An Product must have one or more **Product Statements**. (Fields marked with * are required.)
""")),
                    Div(
                        Formset('statements'),
                        css_class="statements_form"
                    ),
                ),
                css_class='embedded_formset'
            )
        )

##
## Wizard forms
##

class SelectModelForm(CrispyForm):
    ADD_NEW      = "new"
    USE_EXISTING = "use"

    decision = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(),
        initial=ADD_NEW,
        required=True,
        label="Please select an option:"
    )

    @property
    def verbose_name(self):
        return getattr(self._meta.model, 'verbose_name', str(self._meta.model.__name__))

    @property
    def verbose_name_plural(self):
        return getattr(self._meta.model, 'verbose_name_plural', str(self._meta.model.__name__))

    def __init__(self, *args, **kwargs):
        self._meta = self.Meta()
        super().__init__(*args, **kwargs)
        self.fields['decision'].choices = (
            (self.ADD_NEW,      f"Add a new {self.verbose_name}"),
            (self.USE_EXISTING, f"Use an existing {self.verbose_name}"),
        )
        # print("Objects:", len(self.headerTableObjects()))

    def adjustLayout(self):
        self.helper["decision"].wrap(InlineRadios, css_class="col-md-3")

    @classmethod
    def addNew(cls, wizard, step):
        cleaned_data = wizard.get_cleaned_data_for_step(step) or {}
        #print("addNew:", wizard, step, cleaned_data)
        return cleaned_data.get('decision', cls.ADD_NEW) == cls.ADD_NEW
    @classmethod
    def useExisting(cls, wizard, step):
        return not cls.addNew(wizard, step)

    def headerTableObjects(self):
        return self._meta.model.objects.all()

    def modelAppName(self):
        return self._meta.model._meta.app_label

    def modelName(self):
        return self._meta.model._meta.model_name

    class Meta:
        abstract = True

class SelectActivityForm(SelectModelForm):
    class Meta:
        model = Activity

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** is the center of VAST's model. It represents an activity, which must have one (or more) activity steps.

The activity can take place in one or more **events**.

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Activities', self.modelName())}**)"

class SelectEventForm(SelectModelForm):
    class Meta:
        model = Event

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** is an implementation of an Activity. It represents an activity, that spans a period of time, has a hosting organisation and a location, and a specific target group of participants.

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Events', self.modelName())}**)"

class SelectVisitorGroupForm(SelectModelForm):
    class Meta:
        model = VisitorGroup

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** is a representation of an event participants. It represents the target group of event participants, i.e. their age, education level, nationality, language, etc.

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Visitor Groups', self.modelName())}**)"

class SelectVisitorGroupQRCodeForm(SelectModelForm):
    class Meta:
        model = VisitorGroupQRCode

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** generates a QR code that can be used to instantiate a VAST Tool for a specific visitor group, in an activity's event.

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Visitor Groups QR Codes', self.modelName())}**)"


class SelectVisitorForm(SelectModelForm):
    class Meta:
        model = Visitor

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** represents a visitor that has participated in an activity event, and has produced a set of products (one or more products for each activity step).

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Visitors', self.modelName())}**)"

class SelectProductForm(SelectModelForm):
    class Meta:
        model = Product

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** represents a the product a visitor has produced (one or more products for each activity step).

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Products', self.modelName())}**)"

class SelectStatementForm(SelectModelForm):
    class Meta:
        model = Statement

    def headerMarkdown(self):
        return f"""
# {self.verbose_name} Model ({{{{ wizard.steps.step1 }}}}/{{{{ wizard.steps.count }}}})
The **{self.verbose_name}** represents a statement inside a product. In VAST, all results are modelled as statements. A statement associates a subject (i.e. value) to an object (i.e. another value) through a predicate (a relation name).

In this step, please decide if you are going to re-use an existing {self.verbose_name}, or create a new {self.verbose_name}.
"""

    def headerTableMarkdown(self):
        return f"\n\nExisting {self.verbose_name_plural} are shown in the following table: (**{self.getAdminURL('Admin Statements', self.modelName())}**)"

class SelectExceptionForm(SelectModelForm):
    class Meta:
        model = Statement

    def save(commit=True):
        raise Exception("Test Exception")

