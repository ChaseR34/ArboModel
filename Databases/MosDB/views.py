from django.shortcuts import render

from .serializers import MosSerializer
from .models import Pool

from rest_framework import viewsets

from django.core.exceptions import PermissionDenied

# Create your views here.

class MosViewSet(viewsets.ModelViewSet):
    serializer_class = MosSerializer
    queryset = Pool.objects.using("MosquitoDB").filter(id__lte=110)

    # def get_queryset(self):
    #     print(self.queryset)
    #     return self.queryset
