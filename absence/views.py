from rest_framework import viewsets
from django_filters import rest_framework as filters
from absence.models import Absence
from absence.serializers import AbsenceSerializer
from timetable.filters import ScheduledSubjectFilter


class AbsenceViewSet(viewsets.ModelViewSet):
    serializer_class = AbsenceSerializer
    queryset = Absence.objects.all()
    filter_class = ScheduledSubjectFilter


