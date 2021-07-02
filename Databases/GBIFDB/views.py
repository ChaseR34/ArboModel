from django.shortcuts import render

from .serializers import GBIFSerializer
from .models import ArizonaBirds

from rest_framework import viewsets

from django.core.exceptions import PermissionDenied

# Create your views here.

class GBIFViewSet(viewsets.ModelViewSet):
    serializer_class = GBIFSerializer
    queryset = [ArizonaBirds.objects.using("GBIFDB").first()]

    # def get_queryset(self):
    #     print(self.queryset)
    #     return self.queryset
