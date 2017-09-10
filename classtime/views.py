from django.shortcuts import render

from rest_framework import viewsets
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticated

from classtime.filters import ClassTimeFilter
from classtime.models import ClassTime
from classtime.serializers import ClassTimeSerializer
from core.permissions import IsTeacherOrReadOnly


class ClassTimeViewSet(viewsets.ModelViewSet):
    serializer_class = ClassTimeSerializer
    queryset = ClassTime.objects.all()
    filter_class = ClassTimeFilter

