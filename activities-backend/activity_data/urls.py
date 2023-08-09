from django.urls import path

from activity_data import views

urlpatterns = [
    path('save-statements', views.save_statements, name='save-statements'),
    path('save-visitor', views.save_visitor, name='save-visitor'),
]
