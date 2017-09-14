import datetime
import random

from annoying.functions import get_object_or_None
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from absence.models import Absence
from classtime.models import ClassTime
from core.checks import teacher_check, student_check
from core.queries_functions import get_query_dates
from hometask.models import Hometask

from marks.models import Mark, GradeSubject, Student, Grade, Teacher
from marks.serializers import MarkSerializer, GradeSubjectSerializer, StudentSerializer
from register_notifications.models import RegisterNotification
from timetable.filters import ScheduledSubjectFilter
from timetable.models import ScheduledSubject


class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()
    filter_class = ScheduledSubjectFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Mark.objects.all()
        if student_check(user):
            queryset = queryset.filter(student=Student.objects.get(student_user=user)).order_by('date',
                                                                                                'class_time__lesson_start')
        elif teacher_check(user):
            queryset = queryset.filter(grade_subject__teacher__teacher_user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user
        value = request.data['value']
        student_id = request.data['student']
        class_time_id = request.data['class_time']
        date = request.data['date']
        grade_subject_id = request.data['grade_subject']
        RegisterNotification(sender=Teacher.objects.get(teacher_user=user), receiver=Student.objects.get(pk=student_id), value=value,
                             class_time=ClassTime.objects.get(pk=class_time_id),
                             date=date, grade_subject=GradeSubject.objects.get(pk=grade_subject_id)).save()
        return super(MarkViewSet,self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        value = request.data['value']
        student_id = request.data['student']
        class_time_id = request.data['class_time']
        date = request.data['date']
        grade_subject_id = request.data['grade_subject']
        notification = RegisterNotification.objects.get(sender=Teacher.objects.get(teacher_user=user), receiver=Student.objects.get(pk=student_id),
                                                        class_time=ClassTime.objects.get(pk=class_time_id),
                                                        date=date, grade_subject=GradeSubject.objects.get(pk=grade_subject_id))
        notification.value = value
        notification.save()
        return super(MarkViewSet,self).update(request, *args, **kwargs)

    # @list_route(methods=['get'])
    # def grade_subjects(self, request):
    #     user = request.user
    #     queryset = GradeSubject.objects.all().first()
    #     if student_check(user=user):
    #         queryset = GradeSubject.objects.order_by('subject__full_name').filter(grade__student__student_user=user)
    #     serializers = GradeSubjectSerializer(queryset, many=True)
    #     return Response(serializers.data)
    #
    # @list_route(methods=['get'])
    # def marks_dates(self, request):
    #     user = request.user
    #     queryset = Mark.objects.all().first()
    #     dates = queryset.date
    #     if student_check(user=user):
    #         date_from, date_to = get_query_dates(self)
    #         queryset = Mark.objects.filter(student__student_user=user).filter(date__gte=date_from, date__lte=date_to)
    #         dates = [mark.date for mark in queryset]
    #     return JsonResponse(data={"dates": dates})

    # student token = "Authorization: Token 473cd764e73faf62f185b65e05a655eb9323259f"
    @list_route(methods=['get'])
    def student_table_data(self, request):
        user = self.request.user
        if student_check(user=user):
            try:
                date_from, date_to = get_query_dates(self)
            except:
                content = {'bad date': '?date_from:2017-10-01&date_to:2017-10-30'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            marks = Mark.objects.filter(student=Student.objects.get(student_user=user)).filter(date__gte=date_from,date__lte=date_to).\
                order_by('date', 'grade_subject','class_time__lesson_start')
            grade_subjects = GradeSubject.objects.order_by('subject__full_name').filter(
                grade__student__student_user=user)
            dates = []
            date = date_from
            date_delta = datetime.timedelta(days=1)
            while date < date_to + date_delta:
                dates.append(date.strftime("%d-%m"))
                date += date_delta
            marks = MarkSerializer(marks, many=True).data
            grade_subjects = GradeSubjectSerializer(grade_subjects, many=True).data
            content = {'marks': marks, 'grade_subjects': grade_subjects, 'dates': dates}
            return Response(content, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # teacher token = "Authorization: Token 157883759c78b8ec5414fac80e00f812abde8d14"
    @list_route(methods=['get'])
    def teacher_table_data(self, request):
        user = self.request.user
        if teacher_check(user):
            try:
                grade_subject_id = self.request.query_params.get('grade_subject_id')
                date_from, date_to = get_query_dates(self)
            except:
                content = {'bad date or grade subject id ': '?date_from:2017-10-01&date_to:2017-10-30&grade_subject_id=207'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            if grade_subject_id is None:
                return Response({'no correct grade_subject_id'}, status=status.HTTP_400_BAD_REQUEST)
            all_marks = Mark.objects.order_by('date').filter(grade_subject_id=grade_subject_id). \
                filter(date__gte=date_from).filter(date__lte=date_to).order_by('date','student__name')
            grade = get_object_or_None(Grade, gradesubject__id=grade_subject_id)
            dates = [ date.strftime('%d-%m %a') for date in ScheduledSubject.objects.
                filter(grade_subject_id=grade_subject_id).filter(date__gte=date_from).
                filter(date__lte=date_to).values_list('date', flat=True).distinct()]
            students = Student.objects.filter(grade=grade).order_by('name')
            marks = MarkSerializer(all_marks, many=True).data
            students = StudentSerializer(students, many=True).data
            return Response({'marks': marks, 'students': students, 'dates': dates})

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


