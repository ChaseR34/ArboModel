from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import GBIFViewSet

router = DefaultRouter()
router.register("gbif", GBIFViewSet , basename="gbif")
urlpatterns = [
    path('', include(router.urls)),
]