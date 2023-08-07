# https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.shortcuts import render
from django.template.loader import render_to_string

class Formset(LayoutObject):
    template = "formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, context, template_pack=TEMPLATE_PACK):
        formset = None
        ## Get the formset from the form...
        if hasattr(form, self.formset_name_in_context):
            formset = getattr(form, self.formset_name_in_context, None)
        if not formset:
            formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {
            'formset': formset,
            'formset_id': self.formset_name_in_context
        })

