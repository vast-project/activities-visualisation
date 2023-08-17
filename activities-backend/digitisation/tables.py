import django_tables2 as tables
from activity_data.models import *
from django.urls import reverse

def HTMxTable_rows_higlighter(**kwargs):  
    # Add highlight class to rows 
    # when the product is recently updated.
    # Recently updated rows are in the table
    # selection parameter.  
    selected_rows = getattr(kwargs["table"], 'selected_rows  ', None)
    if selected_rows and kwargs["record"].pk in selected_rows:  
        return "highlight-me"  
    return ""

class HTMxTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs={
        'th': {
            'x-data': lambda table: f"""{{ toggleSelection(event) {{
               select_all = !select_all;
               let checkboxes = document.querySelectorAll('#table-container-{table.id} input[name^=\"selected\"]');
               [...checkboxes].map((el) => {{
                 el.checked = select_all;
               }});
               }} }}""",
            '@click': 'toggleSelection()',
            'style': 'cursor: pointer;',
        },
        'th__input': {'class': 'form-check-input', 'x-model': "select_all"},
        'td__input': {
            'class': 'form-check-input',
            'x-model': "isSelected",
            #'@click': 'selectItem()'
        },
    })
    name = tables.Column(linkify=True, attrs={
        'a': {'target': 'blank_'}
    })
    def __init__(self, selected_rows=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id  = self._meta.model.__name__
        # self.id  = self._meta.model._meta.model_name
        self.url = reverse('dashboard-table-model', kwargs={'model': self.id})
        # print(self.id, args, kwargs)
        self.columns['selected'].attrs['td__input'].update({'id': f'selected-{self.id}'})
        self.attrs['class'] += ' table-' + self.id
        self.selected_rows = selected_rows 

    class Meta:
        template_name = "tables/bootstrap_htmx.html"
        fields   = ('selected', 'name', 'created_by')
        sequence = ('selected', '...')
        attrs = {
            'class': 'table table-sm',
        }
        row_attrs = {  
            'class': HTMxTable_rows_higlighter,
            #'@click': 'selectedRow = null',
            'x-data': "{ isSelected: false }",
            ':class': "{ 'highlight-me': isSelected }"
        }
        #show_header = False

class ActivityHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Activity
        #attrs = {"class": "table table-activity"}

class ActivityStepHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = ActivityStep
        #attrs = {"class": "table table-activitystep"}

class EventHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Event
        #attrs = {"class": "table table-event"}

class VisitorGroupHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = VisitorGroup
        #attrs = {"class": "table table-visitorgroup"}

class VisitorHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Visitor
        #attrs = {"class": "table table-visitor"}

class ProductHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Product
        #attrs = {"class": "table table-product"}

class ProductStatementHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = ProductStatement
        #attrs = {"class": "table table-productstatement"}

class StatementHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Statement
        #attrs = {"class": "table table-statement"}
