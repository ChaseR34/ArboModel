from django.shortcuts import render

from .serializers import WeatherSerializer
from .models import WeatherResults

from rest_framework import viewsets

from django.core.exceptions import PermissionDenied

# Create your views here.

class WeatherViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherSerializer
    queryset = WeatherResults.objects.using("WeatherDB").filter(id__lte=10)

