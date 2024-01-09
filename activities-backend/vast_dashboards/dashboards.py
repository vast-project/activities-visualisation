from datetime import datetime, timedelta
from collections import Counter
from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Q
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
import matplotlib.pyplot as plt

from vast_dashboards.data import DashboardData

from activity_data.models import *

from vast_rdf.vast_dam import DAMStoreVAST

from .components import SVGChart
from .serializers import SVGChartSerializer

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
class ActivitySerializer(TableSerializer):
    class Meta:
        title = "Activities"
        columns = {
            "name": "Name",
        }
        order = ["-name"]
        model = Activity

class ActivityStepSerializer(TableSerializer):

    @staticmethod
    def get_data(filters, **kwargs):
        if 'object' in kwargs:
            objects = ActivityStep.objects.filter(activity__pk=kwargs['object'].pk)
        else:
            objects = ActivityStep.objects.all()
        return [{
                    'name': o.name,
                    'stm_name': f'<a href="{o.stimulus.get_dashboard_absolute_url()}" target="_blank">{o.stimulus.name}</a>',
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
            if start == end:
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

class ActivityWordcloudSerialiser(SVGChartSerializer):
    def get_data(self, *args, filters=None, **kwargs) -> Counter:
        if 'object' in kwargs:
            statements = Statement.objects.filter(product__activity_step__activity__pk=kwargs['object'].pk)
            product_statements = ProductStatement.objects.filter(subject__activity_step__activity__pk=kwargs['object'].pk)
        else:
            statements = Statement.objects.all()
            product_statements = ProductStatement.objects.all()
        eng = Counter()
        local = Counter()
        for s in statements:
            eng[s.subject.name] += 1
            eng[s.object.name]  += 1
        for s in product_statements:
            eng[s.object.name]  += 1
        if not len(eng):
            eng['empty'] += 1
        return eng

    def to_svg(self, data):
        layout = {}
        for attr in self.meta_layout_attrs:
            layout[attr] = getattr(self._meta, attr)

        if len(data):
            wordcloud = WordCloud(**layout).generate_from_frequencies(dict(data))
            return wordcloud.to_svg()
        return ""

    class Meta:
        height = 450
        width  = 500

class ActivityWordHistogramSerialiser(ChartSerializer):
    def get_data(self, *args, filters=None, **kwargs) -> pd.DataFrame:
        counter = ActivityWordcloudSerialiser().get_data(*args, filters=filters, **kwargs)
        data = [dict(word=i[0], count=i[1]) for i in counter.most_common()]
        return pd.DataFrame(data)

    def to_fig(self, df):
        fig = px.bar(df, x="word", y="count", color="word")
        fig.update_layout(
            xaxis_title="Value Frequency",
            yaxis_title=None,
        )
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20),)
        return fig

class ActivityProductImagesSerializer(TableSerializer):
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

@register
class ActivitiesDashboard(VASTDashboardMixin, Dashboard):
    welcome = Text(value="VAST Activities")
    # activities_form = Form(form=ActivitiesForm,)
    # animals = Chart(defer=DashboardData.fetch_animals)
    activities_table = Table(value=ActivitySerializer, grid_css_classes="span-12")

    class Meta:
        name = "Activities"

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
            Card("cloud", heading="Value Cloud",  grid_css_classes="span-6"),
            Card("histo", heading="Value Histogram",  grid_css_classes="span-6"),
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
                "value":     ', '.join([f'<a href="{a.europeana_uriref}" target="_blank">&quot;{a.name}&quot;</a>' for a in self.object.europeana_ch_artifact.all()]),
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
