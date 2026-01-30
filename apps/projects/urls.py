from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TravelProjectViewSet

app_name = 'projects'

router = DefaultRouter()
router.register(r'projects', TravelProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]