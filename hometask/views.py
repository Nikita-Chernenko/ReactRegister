from rest_framework import viewsets

from hometask.models import Hometask
from hometask.serializers import HometaskSerializer
from timetable.filters import ScheduledSubjectFilter


class HometaskViewSet(viewsets.ModelViewSet):
    serializer_class = HometaskSerializer
    queryset = Hometask.objects.all()
    filter_class = ScheduledSubjectFilter