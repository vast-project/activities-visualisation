from datetime import datetime, timedelta
from collections import Counter
from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from dashboards.dashboard import Dashboard, ModelDashboard
from dashboards.component import Text, Chart, Table, Form, BasicTable, CTA, Map
from dashboards.component.text import Stat, StatData
from dashboards.component.table import TableSerializer, SerializedTable
from dashboards.component.layout import ComponentLayout, HTML, Card, Header, Div, HR
from dashboards.component.chart import ChartSerializer
from dashboards.forms import DashboardForm
from dashboards.registry import registry

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from wordcloud import WordCloud

from vast_dashboards.data import DashboardData

from activity_data.models import *

from vast_rdf.vast_dam import DAMStoreVAST

from .components import SVGChart
from .serializers import SVGChartSerializer

from dal import autocomplete

def register(cls):
    registry.register(cls)
    return cls

class VASTDashboardMixin:
    def get_context(self, **kwargs) -> dict:
        context = super().get_context(**kwargs)
        context.update({'segment': f'dashboards:vast_dashboards_{self.__class__.__name__.lower()}'})
        # print("VASTDashboard: get_context()", context)
        return context
    # class Media:
    #     js = ("dashboards/js/dashboard.js",
    #           "dashboards/vendor/js/plotly.min.js",
    #           "dashboards/vendor/js/datatables.min.js")
    #     css = {
    #         "all": ("dashboards/vendor/css/datatables.min.css",),
    #     }


class ActivitiesForm(DashboardForm):
    activities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=(
            ("all", "All"),
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
        )
    )
class VASTTableSerializerMixin:
    class Media:
        js = ("dashboards/vendor/js/datatables.min.js",)
        css = {
            "all": ("dashboards/vendor/css/datatables.min.css",),
        }

class ActivitySerializer(VASTTableSerializerMixin, TableSerializer):
    @staticmethod
    def get_data(filters, **kwargs):
        if 'object' in kwargs and kwargs['object']:
            objects = Activity.objects.filter(pk=kwargs['object'].pk)
        else:
            objects = Activity.objects.all()
        if filters and "value" in filters and filters["value"] != "all":
            # Select all products having this value...
            objects = Activity.objects.filter(Q(visitor__product__statement__subject=filters["value"]) |
                                              Q(visitor__product__statement__object=filters["value"])  |
                                              Q(visitor__product__ps_subject__object=filters["value"]) |
                                              Q(visitor__product__productannotation__value=filters["value"])
                                             ).distinct()
        return [{
            'name': f'<a href="{o.get_dashboard_absolute_url()}" target="_blank">{o.name} <i class="fa-solid fa-arrow-up-right-from-square ms-3"></a>',
            'events': Event.objects.filter(activity__pk=o.pk).count(),
            'visitors': Visitor.objects.filter(activity__pk=o.pk).count(),
            'products': Product.objects.filter(activity_step__activity__pk=o.pk).count(),
            'statements': Statement.objects.filter(product__activity_step__activity__pk=o.pk).count() + \
                          ProductStatement.objects.filter(subject__activity_step__activity__pk=o.pk).count(),
        } for o in objects]
    class Meta:
        title = "Activities"
        columns = {
            "name": "Name",
            "events": "Events",
            "visitors": "Participants",
            "products": "Products",
            "statements": "Statements",
        }
        order = ["-name"]
        model = Activity

class ActivityStepSerializer(VASTTableSerializerMixin, TableSerializer):

    @staticmethod
    def get_data(filters, **kwargs):
        if 'object' in kwargs:
            objects = ActivityStep.objects.filter(activity__pk=kwargs['object'].pk)
        else:
            objects = ActivityStep.objects.all()
        return [{
                    'name': f'<a href="{o.get_dashboard_absolute_url()}" target="_blank">{o.name} <i class="fa-solid fa-arrow-up-right-from-square ms-3"></a>',
                    'stm_name': f'<a href="{o.stimulus.get_dashboard_absolute_url()}" target="_blank">{o.stimulus.name} <i class="fa-solid fa-arrow-up-right-from-square ms-3"></a>',
                    'stm_type': o.stimulus.stimulus_type,
                } for o in objects]

    class Meta:
        title = "Activity Steps"
        columns = {
            "name": "Activity Step Name",
            "stm_name": "Stimulus Name",
            "stm_type": "Stimulus Type",
        }
        order = ["-name"]

class EventMapSerializer(ChartSerializer):
    def get_data(self, *args, filters=None, **kwargs) -> pd.DataFrame:
        if 'object' in kwargs:
            objects = Event.objects.filter(activity__pk=kwargs['object'].pk)
        else:
            objects = Event.objects.all()

        return pd.DataFrame(
            [
                {
                    "lat": float(e.location.split(",")[0]),
                    "lon": float(e.location.split(",")[1]),
                    "text": f"{e.city}",
                }
                for e in objects
            ]
        )

    def to_fig(self, data):
        fig = go.Figure()

        if data is None:
            fig.add_trace(go.Scattergeo())
        else:
            fig.add_trace(
                go.Scattergeo(
                    lon=data["lon"],
                    lat=data["lat"],
                    hoverinfo="text",
                    text=data["text"],
                    mode="lines+markers",
                )
            )
            fig.update_layout(
                geo={
                    "lonaxis": {
                        "range": [min(data["lon"]) - 10, max(data["lon"]) + 10],
                    },
                    "lataxis": {
                        "range": [min(data["lat"]) - 10, max(data["lat"]) + 10],
                    },
                }
            )
            fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),)

        return fig
    class Meta:
        title = "Event Locations"

class EventGanttSerialiser(ChartSerializer):
    def get_data(self, *args, filters=None, **kwargs) -> pd.DataFrame:
        if 'object' in kwargs:
            objects = Event.objects.filter(activity__pk=kwargs['object'].pk)
        else:
            objects = Event.objects.all()
        # data = [dict(Task=e.name,
        #              Start=e.date_from if e.date_from else e.date,
        #              Finish=e.date_to if e.date_to else e.date + timedelta(hours=24)) for e in objects]
        data = []
        for e in objects:
            start = e.date_from if e.date_from else e.date
            end   = e.date_to if e.date_to else e.date
            if not start:
                # Use creation date...
                start = e.created
            if not end:
                end = start + timedelta(hours=24)
            if end and start == end:
                end += timedelta(hours=24)
            data.append(dict(Task=f'{e.name} ({e.city})', Start=start, Finish=end, Location=e.city))
        return pd.DataFrame(data)

    def to_fig(self, data):
        fig = px.timeline(data, x_start="Start", x_end="Finish", y="Task")
        #fig.update_layout(autosize=True, width=200, height=200,)
        fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20),)
        return fig

    class Meta:
        title = "Event Timeline"

class ActivityWordMixin:
    @staticmethod
    def get_data_counters(filters=None, **kwargs) -> Counter:
        if 'object' in kwargs:
            statements = Statement.objects.filter(product__activity_step__activity__pk=kwargs['object'].pk)
            product_statements = ProductStatement.objects.filter(subject__activity_step__activity__pk=kwargs['object'].pk)
        else:
            statements = Statement.objects.all()
            product_statements = ProductStatement.objects.all()
        counter = Counter()
        for s in statements:
            counter[(s.subject.name, s.subject.name_local)] += 1
            counter[(s.object.name,  s.object.name_local)]  += 1
        for s in product_statements:
            counter[(s.object.name, s.object.name_local)]   += 1
        if not len(counter):
            counter[('empty', 'empty')] += 1
        return counter

class ActivityWordcloudSerialiser(ActivityWordMixin, SVGChartSerializer):
    def get_data(self, *args, filters=None, **kwargs) -> Counter:
        return self.get_data_counters(filters=filters, **kwargs)

    def to_svg(self, data):
        layout = {}
        for attr in self.meta_layout_attrs:
            layout[attr] = getattr(self._meta, attr)

        if len(data):
            wordcloud = WordCloud(**layout).generate_from_frequencies({w[0][0]:w[1] for w in data.most_common()})
            return wordcloud.to_svg()
        return ""

    class Meta:
        height = 450
        width  = 500

class ActivityWordHistogramSerialiser(ActivityWordMixin, ChartSerializer):
    def get_data(self, *args, filters=None, **kwargs) -> pd.DataFrame:
        counter = self.get_data_counters(filters=filters, **kwargs)
        data = [dict(word=i[0][0], count=i[1]) for i in counter.most_common()]
        return pd.DataFrame(data)

    def to_fig(self, df):
        fig = px.bar(df, x="word", y="count", color="word")
        fig.update_layout(
            yaxis_title="Value Frequency",
            xaxis_title=None,
        )
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20),)
        return fig

class ActivityWordTableSerialiser(ActivityWordMixin, VASTTableSerializerMixin, TableSerializer):
    @staticmethod
    def get_data(filters, **kwargs):
        counter = ActivityWordTableSerialiser.get_data_counters(filters=filters, **kwargs)
        c = 0
        return [{'id':i+1, 'value': w[0][0], 'local': w[0][1], 'freq': w[1]} for i,w in enumerate(counter.most_common())]

    class Meta:
        title = "Values"
        columns = {
            "id": "ID",
            "value": "Value",
            "local": "Value (local)",
            "freq":  "Frequency",
        }
        order = ["-freq"]


class ActivityProductImagesSerializer(VASTTableSerializerMixin, TableSerializer):
    @staticmethod
    def chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    @staticmethod
    def get_data(filters, **kwargs):
        if 'object' in kwargs:
            objects = Product.objects.filter(activity_step__activity__pk=kwargs['object'].pk)
        else:
            objects = Product.objects.all()
        objects = filter(lambda o: o.image_uriref, objects)
        data = []
        for chunk in ActivityProductImagesSerializer.chunker(list(objects), 8):
            col = 1
            row = {}
            for o in chunk:
                row.update({
                    f'name{col}': o.name,
                    f'img{col}': f'<a href="{o.image_uriref}" data-toggle="tooltip" title="{o.name}" target="_blank"><img src="{o.image_uriref}" alt="{o.name}" width="100px" height="auto"></a>',
                })
                col +=1
            data.append(row)
        return data

    class Meta:
        title = "Activity Product Gallery"
        columns = {
            "img1": "Image",
            "img2": "Image",
            "img3": "Image",
            "img4": "Image",
            "img5": "Image",
            "img6": "Image",
            "img7": "Image",
            "img8": "Image",
        }

class SearchValuesForm(DashboardForm):
    value = forms.ModelChoiceField(queryset=Concept.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['search'].widget.url = reverse('dashboard-autocomplete-model', kwargs={'model': 'Concept'})
    class Meta:
        widgets = {
            'value': autocomplete.ModelSelect2(url='dashboard-autocomplete-model-concept', attrs={
                # Set some placeholder
                'data-placeholder': 'Autocomplete ...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 3,
            },)
        }
    class Media:
        js = ('admin/js/vendor/select2/select2.full.js',
              'autocomplete_light/autocomplete_light.min.js',
              'autocomplete_light/select2.min.js')
        css = {'screen': (
              'admin/css/vendor/select2/select2.min.css',
              'admin/css/autocomplete.css',
              'autocomplete_light/select2.css',
             ),
        }

@register
class ActivitiesDashboard(VASTDashboardMixin, Dashboard):
    activities_table = Table(value=ActivitySerializer, css_classes="table table-hover align-middle table-left table-first-w-50 table-not-first-align-center", grid_css_classes="span-12")

    class Meta:
        name = "Activities"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Card("activities_table", 
                 heading = mark_safe("<i class=\"fa-solid fa-building-columns me-3\"></i> VAST Activities"),
                 css_classes="card", grid_css_classes="span-12"
            ),
        )

@register
class ValuesDashboard(VASTDashboardMixin, Dashboard):
    value = Form(value='', form=SearchValuesForm, dependents=["activities_table"],)
    activities_table = Table(value=ActivitySerializer, css_classes="table table-hover align-middle table-left table-first-w-50 table-not-first-align-center", grid_css_classes="span-12")

    class Meta:
        name = "Values"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Card("value", 
                 heading = mark_safe("<i class=\"fa-solid fa-building-columns me-3\"></i> Values Search"),
                 css_classes="card", grid_css_classes="span-12"
            ),
            Card("activities_table", 
                 heading = mark_safe("<i class=\"fa-solid fa-building-columns me-3\"></i> VAST Activities"),
                 css_classes="card", grid_css_classes="span-12"
            ),
        )

# https://www.djangodashboards.com/
@register
class ActivityDashboard(VASTDashboardMixin, ModelDashboard):
    # name    = Text(mark_safe=True)
    details = BasicTable(css_classes="table table-hover align-middle table-description", grid_css_classes="span-12")
    steps   = Table(value=ActivityStepSerializer, css_classes="table table-hover align-middle table-left font-size-075", grid_css_classes="span-12")
    who     = Stat()
    where   = Map(value=EventMapSerializer)
    when    = Chart(value=EventGanttSerialiser)

    cloud   = SVGChart(value=ActivityWordcloudSerialiser)
    table   = Table(value=ActivityWordTableSerialiser)
    histo   = Chart(value=ActivityWordHistogramSerialiser)

    gallery = Table(value=ActivityProductImagesSerializer, page_size=2, searching=False, ordering=False, css_classes="table align-middle", grid_css_classes="span-12")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dam = DAMStoreVAST()
        json_data = dam.get_resource(self.object.document_resource_id)
        self.thm_url = dam.get_size(json_data, size='thm')
        if self.thm_url:
            self.thm_url = self.thm_url['url']
        del dam

    class Meta:
        name = "Activity"
        model = Activity

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Card(
                 Div("details",
                     css_classes={"wrapper":"table-responsive"}, grid_css_classes="span-12"),
                 HR(),
                 Header(heading="Steps and Stimuli", size=4),
                 Div("steps",
                     css_classes={"wrapper":"table-responsive"}, grid_css_classes="span-6"),
                 heading = mark_safe("<i class=\"fa-solid fa-building-columns me-3\"></i>Activity"),
                 #actions = [("http://google.com", "Google")],
                 css_classes="card", grid_css_classes="span-12"
            ),
            Card("who",   heading="Who",   grid_css_classes="span-12"),
            Card("where", heading="Where", grid_css_classes="span-6"),
            Card("when",  heading="When",  grid_css_classes="span-6"),
            Card("cloud", heading="Values Cloud",  grid_css_classes="span-6"),
            Card("histo", heading="Values Histogram",  grid_css_classes="span-6"),
            Card(Div("table", css_classes={"wrapper":"table-responsive"}, grid_css_classes="span-12"),
                 heading="Values Frequencies", grid_css_classes="span-12"),
            Card(Div("gallery", css_classes={"wrapper":"table-responsive"}, grid_css_classes="span-12"),
                 heading="Products Gallery", grid_css_classes="span-12"),

            grid_css_classes="span-12"
        )

    def get_name_value(self, **kwargs):
        content = f"<h4><i class=\"fa-solid fa-building-columns\"></i> Activity: &quot;{self.object.name}&quot;</h4>"
        return content

    def get_thm_value(self, **kwards):
        if self.object.document_uriref:
            return f'<a href="{self.object.document_uriref}" target="_blank"><img src="{self.thm_url}" width="141px"</a>'
        else:
            return ""

    def get_details_value(self, **kwargs):
        data = [
            {
                "attribute": "<strong>Description</strong>:",
                "value":     self.object.description,
                "handbook":  self.get_thm_value(**kwargs),
            },
            {
                "attribute": "<strong>Age</strong>:",
                "value":     self.object.age,
                "handbook":  ""
            },
            {
                "attribute": "<strong>VAST Annotated Cultural Heritage Artifacts</strong>:",
                "value":     ', '.join([a.name for a in self.object.ch_artifact.all()]),
                "handbook":  ""
            },
            {
                "attribute": "<strong>Europeana Annotated Cultural Heritage Artifacts</strong>:",
                "value":     ', '.join([f'<a href="{a.europeana_uriref}" target="_blank">&quot;{a.name}&quot; <i class="fa-solid fa-arrow-up-right-from-square ms-1 me-1"></i></a>' for a in self.object.europeana_ch_artifact.all()]),
                "handbook":  ""
            },
        ]
        return SerializedTable(
            columns={"attribute": "<i class=\"fa-solid fa-building-columns\"></i> Activity:",
                     "value": self.object.name, "handbook": "Handbook"},
            data=data,
            columns_datatables=[],
            order=[],
        )

    def get_who_value(self, **kwargs):
        s_c  = Statement.objects.filter(product__activity_step__activity__pk=self.object.pk).count()
        ps_c = ProductStatement.objects.filter(subject__activity_step__activity__pk=self.object.pk).count()
        sep = ", "
        content = f"<strong>Events</strong>: {Event.objects.filter(activity__pk=self.object.pk).count()}"
        content += sep
        content += f"<strong>Participants</strong>: {Visitor.objects.filter(activity__pk=self.object.pk).count()}"
        content += sep
        content += f"<strong>Products</strong>: {Product.objects.filter(activity_step__activity__pk=self.object.pk).count()}"
        content += sep
        content += f"<strong>Statements</strong>: {s_c + ps_c}"
        sub_content = f"<strong>Statements</strong>: {s_c}"
        sub_content += sep
        sub_content += f"<strong>Product Statements</strong>: {ps_c}"

        return StatData(
            text=mark_safe(content),
            sub_text = mark_safe(sub_content),
        )

class VASTModelDashboard(VASTDashboardMixin, ModelDashboard):
    name    = Text(mark_safe=True, grid_css_classes="span-12")
    details = BasicTable(css_classes="table table-hover align-middle table-description-2", grid_css_classes="span-12")

    def get_icon(self, classes=''):
        return f'<i class="fa-solid fa-box {classes}"></i>'

    def get_class_name(self):
        return self._meta.model._meta.model.__name__

    def get_name_value(self, **kwargs):
        content = f'<h4>{self.get_icon("me-3")} {self.get_class_name()}: &quot;{self.object.name}&quot;</h4>'
        return content

    def get_details_columns(self):
        return {"attribute": self.get_icon() + ' ' + self.get_class_name() + ':',
                     "value": self.object.name}
    def get_details_attributes(self):
        print([f.name for f in self.object._meta.get_fields()])
        return [f.name for f in self.object._meta.get_fields()]
    def get_details_data_attribute_hide_fields(self):
        return ('id', 'uuid', 'name_md5', 'created', 'updated', 'created_by')
    def get_details_data_attribute_show(self, a, v):
        if a in self.get_details_data_attribute_hide_fields():
            return False
        return True if v else False
    def get_details_data_attribute_name(self, a, v):
        return f"<strong>{a.replace('_', ' ').title()}</strong>:"
    def get_details_data_attribute_value(self, a, v):
        if isinstance(v, AutoUpdateTimeFields):
            url = v.get_dashboard_absolute_url()
            if url:
                return f'<a href="{url}" target="_blank">{v.name} <i class="fa-solid fa-arrow-up-right-from-square ms-3"></i></a>'
            return v.name
        return f'<a href="{v}" target="_blank">{v}</a>' if isinstance(v, str) and v.startswith('http') else v
    def get_details_data(self):
        for a in self.get_details_attributes():
            print(a, getattr(self.object, a, None), type(getattr(self.object, a, None)))
        return [{
                    "attribute": self.get_details_data_attribute_name(a, v),
                    "value":     self.get_details_data_attribute_value(a, v),
                } for a in self.get_details_attributes() if (self.get_details_data_attribute_show(a, v := getattr(self.object, a, None)))]

    def get_details_value(self, **kwargs):
        return SerializedTable(
            columns=self.get_details_columns(),
            data=self.get_details_data(),
            columns_datatables=[],
            order=[],
        )

    class _Layout(Dashboard.Layout):
        def __init__(self, dashboard):
            self.dashboard = dashboard
            self.components = ComponentLayout(
                Card("name", "details",
                    heading = mark_safe(f'{self.dashboard.get_icon("me-3")} {self.dashboard.get_class_name()}'),
                    css_classes="card", grid_css_classes="span-12"
                ),
            )
    def Layout(self):
        return self._Layout(self)

@register
class StimulusDashboard(VASTModelDashboard):

    def get_icon(self, classes=''):
        match self.object.stimulus_type:
            case 'Document':
                icon = f'<i class="fa-regular fa-file {classes}"></i>'
            case 'Segment':
                icon = f'<i class="fa-solid fa-bars-staggered {classes}"></i>'
            case 'Image':
                icon = f'<i class="fa-regular fa-image {classes}"></i>'
            case 'Audio':
                icon = f'<i class="fa-regular fa-file-audio {classes}"></i>'
            case 'Video':
                icon = f'<i class="fa-regular fa-file-video {classes}"></i>'
            case 'Game':
                icon = f'<i class="fa-solid fa-gamepad {classes}"></i>'
            case 'Presentation':
                icon = f'<i class="fa-solid fa-person-chalkboard {classes}"></i>'
            case 'Tool':
                icon = f'<i class="fa-solid fa-gear {classes}"></i>'
            case 'Questionnaire':
                icon = f'<i class="fa-solid fa-question {classes}"></i>'
            case 'Live Performance':
                icon = f'<i class="fa-solid fa-ear-listen {classes}"></i>'
            case 'Senses':
                icon = ''
            case 'Template':
                icon = f'<i class="fa-regular fa-file-lines {classes}"></i>'
            case 'Template Mind-Map':
                icon = f'<i class="fa-solid fa-diagram-project {classes}"></i>'
            case _:
                icon = ''
        return icon

    def get_name_value(self, **kwargs):
        return f'<h4>{self.get_icon("me-6 fs-1")} {self.get_class_name()}: &quot;{self.object.name}&quot;</h4>'

    class Meta:
        model = Stimulus

@register
class ActivityStepDashboard(VASTModelDashboard):
    class Meta:
        model = ActivityStep

@register
class EventDashboard(VASTModelDashboard):
    class Meta:
        model = Event

@register
class VisitorGroupDashboard(VASTModelDashboard):
    class Meta:
        model = VisitorGroup

@register
class VisitorDashboard(VASTModelDashboard):
    class Meta:
        model = Visitor

@register
class VirtualVisitorDashboard(VASTModelDashboard):
    class Meta:
        model = VirtualVisitor

@register
class ProductDashboard(VASTModelDashboard):
    class Meta:
        model = Product

@register
class ProductStatementDashboard(VASTModelDashboard):
    class Meta:
        model = ProductStatement

@register
class StatementDashboard(VASTModelDashboard):
    class Meta:
        model = Statement

@register
class QuestionnaireEntryDashboard(VASTModelDashboard):
    class Meta:
        model = QuestionnaireEntry

@register
class QuestionnaireQuestionDashboard(VASTModelDashboard):
    class Meta:
        model = QuestionnaireQuestion

@register
class QuestionnaireAnswerDashboard(VASTModelDashboard):
    class Meta:
        model = QuestionnaireAnswer

@register
class AgeDashboard(VASTModelDashboard):
    class Meta:
        model = Age

@register
class EducationDashboard(VASTModelDashboard):
    class Meta:
        model = Education

@register
class NationalityDashboard(VASTModelDashboard):
    class Meta:
        model = Nationality

@register
class OrganisationDashboard(VASTModelDashboard):
    class Meta:
        model = Organisation

@register
class OrganisationTypeDashboard(VASTModelDashboard):
    class Meta:
        model = OrganisationType

@register
class LanguageDashboard(VASTModelDashboard):
    class Meta:
        model = Language

@register
class ClassDashboard(VASTModelDashboard):
    class Meta:
        model = Class

@register
class ContextDashboard(VASTModelDashboard):
    class Meta:
        model = Context

@register
class NatureDashboard(VASTModelDashboard):
    class Meta:
        model = Nature

@register
class CulturalHeritageArtifactDashboard(VASTModelDashboard):
    class Meta:
        model = CulturalHeritageArtifact

@register
class EuropeanaCulturalHeritageArtifactDashboard(VASTModelDashboard):
    class Meta:
        model = EuropeanaCulturalHeritageArtifact

@register
class GenderDashboard(VASTModelDashboard):
    class Meta:
        model = Gender

@register
class ProductTypeDashboard(VASTModelDashboard):
    class Meta:
        model = ProductType

@register
class ConceptTypeDashboard(VASTModelDashboard):
    class Meta:
        model = ConceptType

@register
class ConceptDashboard(VASTModelDashboard):
    class Meta:
        model = Concept

@register
class PredicateDashboard(VASTModelDashboard):
    class Meta:
        model = Predicate

@register
class ProductAnnotationDashboard(VASTModelDashboard):
    class Meta:
        model = ProductAnnotation

@register
class DigitisationApplicationDashboard(VASTModelDashboard):
    class Meta:
        model = DigitisationApplication

@register
class VisitorGroupQRCodeDashboard(VASTModelDashboard):
    class Meta:
        model = VisitorGroupQRCode

#registry.register(ActivitiesDashboard)
#registry.register(ActivityDashboard)
#registry.register(StimulusDashboard)
#registry.register(ActivityStepDashboard)
#registry.register(EventDashboard)
#registry.register(VisitorGroupDashboard)
#registry.register(VisitorDashboard)
#registry.register(VirtualVisitorDashboard)
#registry.register(ProductDashboard)
#registry.register(ProductStatementDashboard)
#registry.register(StatementDashboard)
#registry.register(QuestionnaireEntryDashboard)
#registry.register(QuestionnaireQuestionDashboard)
#registry.register(QuestionnaireAnswerDashboard)
#registry.register(AgeDashboard)
