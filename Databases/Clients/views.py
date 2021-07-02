from django.shortcuts import render
from django.views import View

from .serializers import ClientSerializer
from .models import Client

from rest_framework import viewsets

from django.core.exceptions import PermissionDenied


# Create your views here.



class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        print("getting a request")
        print(self.request)
        print("user printed")
        print(self.request.user)
        print(self.request.data)
        print("after")
        print(self.queryset.filter(created_by=self.request.user))
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()
