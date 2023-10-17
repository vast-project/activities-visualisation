from django.urls import path

from activity_data import views

urlpatterns = [
    path('save-statements', views.save_statements, name='save-statements'),
    path('save-visitor', views.save_visitor, name='save-visitor'),
    path('ftm/save-statements', views.save_ftm_statements, name="save-ftm-statements"),
    path('save-values-workshop-data', views.save_values_workshop, name="save-values-workshop-data"),
]
