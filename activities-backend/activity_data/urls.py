from django.urls import include, path
#from rest_framework import routers
from activity_data import views

#irouter = routers.DefaultRouter()
#router.register(r'imss_mindmap',  views.StoreActivityData)

urlpatterns = [
    path('products',     views.ProductView.as_view(), name="products"),
    path('imss_mindmap', views.StoreActivityData.as_view(), name="mindmap"),
    path('saveproduct', views.saveproduct, name='saveproduct'),
    path('savevisitor', views.savevisitor, name='savevisitor')
]
