import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from core.checks import student_check, teacher_check
from core.queries_functions import get_query_dates
from hometask.models import Hometask
from hometask.serializers import HometaskSerializer
from marks.models import Student
from timetable.filters import ScheduledSubjectFilter
from marks.views import  MarkViewSet


class HometaskViewSet(viewsets.ModelViewSet):
    serializer_class = HometaskSerializer
    queryset = Hometask.objects.all()
    filter_class = ScheduledSubjectFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Hometask.objects.all()
        if student_check(user):
            date_from,date_to = get_query_dates(self)
            queryset =  queryset.filter(grade_subject__grade__student= Student.objects.get(student_user=user)).\
                filter(date__gte=date_from,date_lte=date_to)
            return queryset
        elif teacher_check(user):
            date_from,date_to = get_query_dates(self)
            queryset = queryset.filter(grade_subject__teacher__teacher_user=user).\
                filter(date__gte=date_from,date__lte=date_to)
        return queryset



