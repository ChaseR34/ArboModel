from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MosViewSet

router = DefaultRouter()
router.register("mos", MosViewSet, basename="mos")
urlpatterns = [
    path('', include(router.urls)),
]