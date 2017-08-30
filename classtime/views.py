from django.shortcuts import render

from rest_framework import viewsets
from django_filters import rest_framework

from classtime.filters import ClassTimeFilter
from classtime.models import ClassTime
from classtime.serializers import ClassTimeSerializer


class ClassTimeViewSet(viewsets.ModelViewSet):
    serializer_class = ClassTimeSerializer
    queryset = ClassTime.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = ClassTimeFilter

