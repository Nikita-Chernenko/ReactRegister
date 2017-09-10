from django.shortcuts import render
from rest_framework import viewsets

from core.checks import student_check, teacher_check
from core.queries_functions import get_query_dates
from marks.models import Student
from timetable.filters import ScheduledSubjectFilter
from timetable.models import ScheduledSubject
from timetable.serializers import TimetableSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = TimetableSerializer
    queryset = ScheduledSubject.objects.all()
    filter_class = ScheduledSubjectFilter

    def get_queryset(self):
        queryset = ScheduledSubject.objects.all()
        user = self.request.user
        if student_check(user):
            date_from,date_to = get_query_dates(self)
            queryset = queryset.filter(grade_subject__grade__student=Student.objects.get(student_user=user)).\
                filter(date__gte=date_from,date__lte=date_to)
        elif teacher_check(user):
            date_from,date_to  = get_query_dates(self)
            queryset = queryset.filter(grade_subject__teacher__teacher_user=user).\
                filter(date__gte=date_from,date__lte=date_to)
        return queryset