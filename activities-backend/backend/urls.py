"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from backend import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

router = routers.DefaultRouter()
router.register(r'languages',            views.LanguageViewSet)
router.register(r'organisation_types',   views.OrganisationTypeViewSet)
router.register(r'organisations',        views.OrganisationViewSet)
router.register(r'events',               views.EventViewSet)
router.register(r'contexts',             views.ContextViewSet)
router.register(r'natures',              views.NatureViewSet)
router.register(r'educations',           views.EducationViewSet)
router.register(r'activities',           views.ActivityViewSet)
router.register(r'stimuli',              views.StimulusViewSet)
router.register(r'activity_steps',       views.ActivityStepViewSet)
router.register(r'ages',                 views.AgeViewSet)
router.register(r'genders',              views.GenderViewSet)
router.register(r'nationalities',        views.NationalityViewSet)
router.register(r'classes',              views.ClassViewSet)
router.register(r'visitor_groups',       views.VisitorGroupViewSet)
router.register(r'visitors',             views.VisitorViewSet)
router.register(r'product_types',        views.ProductTypeViewSet)
router.register(r'products',             views.ProductViewSet)
router.register(r'concepts',             views.ConceptViewSet)
router.register(r'predicates',           views.PredicateViewSet)
router.register(r'statements',           views.StatementViewSet)
router.register(r'users',                views.UserViewSet)
router.register(r'groups',               views.GroupViewSet)

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/',      include('activity_data.urls')),
    path('rest/',     include(router.urls), name="rest"),
    path('', RedirectView.as_view(url='rest/', permanent=False), name='index')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
