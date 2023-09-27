import django_tables2 as tables
from activity_data.models import *
from django.urls import reverse

def HTMxTable_show_args(result="", *args, **kwargs):
    print(args, kwargs)
    return result

def HTMxTable_row_x_data(**kwargs):
    row_index = int(repr(kwargs["table"]._counter)[6:-1]) - len(kwargs["table"].paginated_rows) - 1
    return f"{{ rowIndex: {row_index} }}"

def HTMxTable_row_x_init(**kwargs):
    # table = kwargs["table"]
    selected_rows  = getattr(kwargs["table"], 'selected_rows', None)
    if selected_rows and kwargs["record"].pk in selected_rows:
        # print("HTMxTable_row_x_init:", table.id, selected_rows, kwargs["record"].pk, "TRUE")
        return "checkboxes[rowIndex].isChecked = true"
    # print("HTMxTable_row_x_init:", table.id, selected_rows, kwargs["record"].pk, "FALSE")
    return "checkboxes[rowIndex].isChecked = false"

class HTMxTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs={
        'th__input': {'class': 'form-check-input',
                      '@change':"toggleAll", ':checked':"checkboxes.length && checkboxes.every(cb => cb.isChecked)",
                      ':inditerminate':"checkboxes.some(cb => cb.isChecked)"},
        'td__input': {
            'class':   'form-check-input',
            'x-model': 'checkboxes[rowIndex].isChecked',
            #'x-text':  'checkboxes[rowIndex].isChecked',
            '@click':  '$nextTick(() => $store.dashboardInteractiveFiltering.notify())',
        },
        'td': {
            #'x-data' : HTMxTable_show_args,
        },
    })
    name = tables.Column(linkify=True, attrs={
        'a': {'target': 'blank_'}
    })
    graphdb = tables.URLColumn(verbose_name="@", orderable=False, text=lambda record: record.get_repository_url(attrs={
        'target': 'blank_', 'class': 'graphdb_link_table'
    }))
    def __init__(self, selected_rows=None, selection_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id  = self._meta.model.__name__
        # self.id  = self._meta.model._meta.model_name
        self.url = reverse('dashboard-table-model', kwargs={'model': self.id})
        # print(self.id, args, kwargs)
        self.columns['selected'].attrs['td__input'].update({'id': f'selected-{self.id}'})
        self.columns['selected'].attrs['td__input']['x-init'] = f'$watch("checkboxes[rowIndex].isChecked", value => $store.dashboardInteractiveFiltering.addPK("{self.id}", $el.value, value));'
        self.attrs['class'] += ' table-' + self.id
        if selection_data:
            extra_selected_rows = selection_data.get(self.id, None)
            if extra_selected_rows:
                if selected_rows:
                    selected_rows.extend(extra_selected_rows)
                else:
                    selected_rows = extra_selected_rows
        self.selected_rows  = selected_rows
        self.selection_data = selection_data
        # print(self.id, selected_rows, selection_data, args, kwargs)

    class Meta:
        template_name = "tables/bootstrap_htmx.html"
        fields   = ('selected', 'name', 'graphdb', 'created_by')
        sequence = ('selected', '...')
        attrs = {
            'class': 'table table-sm table-hover',
        }
        row_attrs = {
            'x-data': HTMxTable_row_x_data,
            'x-init': HTMxTable_row_x_init,
            ':class': "{ 'highlight-me table-primary': checkboxes[rowIndex].isChecked }",
            '@click': "checkboxes[rowIndex].isChecked = !checkboxes[rowIndex].isChecked; $nextTick(() => $store.dashboardInteractiveFiltering.notify())",
        }
        #show_header = False

class ActivityHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Activity

class ActivityStepHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = ActivityStep

class EventHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Event

class VisitorGroupHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = VisitorGroup

class VisitorHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Visitor

class ProductHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Product

class ProductStatementHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = ProductStatement

class StatementHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Statement

class QuestionnaireEntryHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = QuestionnaireEntry

class QuestionnaireQuestionHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = QuestionnaireQuestion

class QuestionnaireAnswerHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = QuestionnaireAnswer
