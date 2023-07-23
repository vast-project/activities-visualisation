from django.urls import path

from activity_data import views

urlpatterns = [
    path('products', views.ProductView.as_view(), name="products"),
    path('imss_mindmap', views.StoreActivityData.as_view(), name="mindmap"),
    path('saveproduct', views.saveproduct, name='saveproduct'),
    path('savevisitor', views.savevisitor, name='savevisitor'),
    path('save-statements', views.save_statements, name='save-statements'),
]
