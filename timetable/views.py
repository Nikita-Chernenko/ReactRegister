from django.shortcuts import render
from rest_framework import viewsets

from timetable.filters import ScheduledSubjectFilter
from timetable.models import ScheduledSubject
from timetable.serializers import TimetableSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = TimetableSerializer
    queryset = ScheduledSubject.objects.all()
    filter_class = ScheduledSubjectFilter