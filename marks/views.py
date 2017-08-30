from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import list_route

from marks.serializers import MarkSerializer, GradeSubjectSerializer
from marks.models import Mark, GradeSubject, Student
from timetable.filters import ScheduledSubjectFilter


class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScheduledSubjectFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Mark.objects.all()
        if not user.is_anonymous:
            if user.staff == "S":
                queryset = queryset.filter(student=Student.objects.get(student_user=user)).order_by('date','class_time__lesson_start')
            elif user.staff == "T":
                grade_subject_id = self.request.query_params.get("grade_subject_id",None)
                queryset = queryset.filter(grade_subject_id=grade_subject_id)
        return queryset
    @list_route(methods=['get'])
    def grade_subjects(self,request):
        user = request.user
        queryset = GradeSubject.objects.all().first()
        if not user.is_anonymous and user.staff == 'S':
            queryset = GradeSubject.objects.filter('subject__full_name').filter(grade__student=user)
        serializers = GradeSubjectSerializer(queryset,many=True)
        return  Response(serializers.data)

    @list_route(methods=['get'])
    def marks_dates(self,request):
        user = request.user
        queryset = Mark.objects.all().first()
        dates = queryset.date
        if not user.is_anonymous and user.staff == 'S':
            queryset = Mark.objects.filter(student=user)
            dates = [mark.date for mark in queryset]
        return JsonResponse(data = {"dates":dates})


