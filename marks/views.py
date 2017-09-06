import datetime

from django.core import serializers
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.decorators import list_route

from marks.serializers import MarkSerializer, GradeSubjectSerializer, SubjectSerializer
from marks.models import Mark, GradeSubject, Student
from timetable.filters import ScheduledSubjectFilter
from annoying.functions import get_object_or_None


class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScheduledSubjectFilter

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            queryset = Mark.objects.all()
            if user.staff == "S":
                queryset = queryset.filter(student=Student.objects.get(student_user=user)).order_by('date',
                                                                                                    'class_time__lesson_start')
            elif user.staff == "T":
                grade_subject_id = self.request.query_params.get("grade_subject_id", None)
                queryset = queryset.filter(grade_subject_id=grade_subject_id)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_query_dates(self):
        date_from = datetime.datetime.strptime(self.request.query_params.get("data_from", "8.09.2017").strip(),
                                               "%d.%m.%Y").date()
        date_to = datetime.datetime.strptime(self.request.query_params.get("data_to", "12.09.2017").strip(),
                                             "%d.%m.%Y").date()
        return date_from, date_to

    @list_route(methods=['get'])
    def grade_subjects(self, request):
        user = request.user
        queryset = GradeSubject.objects.all().first()
        if self.student_check(user=user):
            queryset = GradeSubject.objects.order_by('subject__full_name').filter(grade__student__student_user=user)
        serializers = GradeSubjectSerializer(queryset, many=True)
        return Response(serializers.data)

    @list_route(methods=['get'])
    def marks_dates(self, request):
        user = request.user
        queryset = Mark.objects.all().first()
        dates = queryset.date
        if self.student_check(user=user):
            date_from, date_to = self.get_query_dates()
            queryset = Mark.objects.filter(student__student_user=user).filter(date__gte=date_from, date__lte=date_to)
            dates = [mark.date for mark in queryset]
        return JsonResponse(data={"dates": dates})

    # @list_route(methods=['get'])
    # def marks_for_student_table(self, request):
    #     if self.student_check(user=self.request.user):
    #         try:
    #             date_from,date_to = self.get_query_dates()
    #         except:
    #             content = {'bad date': 'date_from:"01.10.2017", date_to:"30.10.2017"'}
    #             return Response(content, status=status.HTTP_400_BAD_REQUEST)
    #
    #         student = get_object_or_None(Student,student_user=request.user)
    #         all_marks = Mark.objects.order_by('date').filter(student=student). \
    #             filter(date__gte=date_from).filter(date__lte=date_to)
    #         dates = []
    #         date = date_from
    #         date_delta = datetime.timedelta(days=1)
    #         while date < date_to + date_delta:
    #             dates.append(date.strftime("%d-%m"))
    #             date += date_delta
    #
    #         subjects = list(GradeSubject.objects.filter(grade__student=student).order_by('subject__full_name'))
    #         all_marks_list = list([all_marks.filter(grade_subject=subject) for subject in subjects])
    #         i = 1
    #         while (i < len(subjects)):
    #             if subjects[i - 1].subject == subjects[i].subject:
    #                 if len(all_marks_list[i - 1]) >= len(all_marks_list[i]):
    #                     subjects.remove(subjects[i])
    #                     all_marks_list.remove(all_marks_list[i])
    #                 else:
    #                     subjects.remove(subjects[i - 1])
    #                     all_marks_list.remove(all_marks_list[i - 1])
    #                 i -= 1
    #             i += 1
    #         all_marks_index = 0
    #         subjects_marks = []
    #         for subject in subjects:
    #             marks = all_marks_list[all_marks_index]
    #             all_marks_index += 1
    #             marks_index = 0
    #             marks_to_send = []
    #             date = date_from
    #             while date <= date_to + date_delta:
    #                 if marks_index > 0 and marks_index < len(marks) and marks[marks_index].date == marks[
    #                             marks_index - 1].date:
    #                     marks_to_send[len(marks_to_send) - 1]+= "/"  + str(marks[marks_index].value)
    #                     date = marks[marks_index].date
    #                     marks_index += 1
    #                     date += date_delta
    #                     continue
    #                 elif date >= date_to and len(marks_to_send) == len(dates):
    #                     break
    #                 elif marks_index < len(marks) and marks[marks_index].date == date:
    #                     marks_to_send.append(str(marks[marks_index].value))
    #                     marks_index += 1
    #                 else:
    #                     marks_to_send+= " "
    #                 date += date_delta
    #             subjects_marks+= marks_to_send
    #         subjects = SubjectSerializer([subject.subject for subject in subjects],many=True).data
    #         # content = JsonResponse({'dates': dates, 'subjects_marks': subjects_marks,'subjects':subjects})
    #         return Response({'subjects':subjects, 'marks':subjects_marks,'dates':dates},status=status.HTTP_200_OK)
    #     else:
    #         content = {'bad_user': 'user is not a student'}
    #         return Response(content, status=status.HTTP_403_FORBIDDEN)
    @list_route(methods=['get'])
    def student_table_data(self,request):
        user = self.request.user
        if self.student_check(user=user):
            try:
                date_from, date_to = self.get_query_dates()
            except:
                content = {'bad date': 'date_from:"01.10.2017", date_to:"30.10.2017"'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            marks = Mark.objects.filter(student=Student.objects.get(student_user=user)). \
                order_by('date', 'class_time__lesson_start')
            grade_subjects = GradeSubject.objects.order_by('subject__full_name').filter(grade__student__student_user=user)
            dates = []
            date = date_from
            date_delta = datetime.timedelta(days=1)
            while date < date_to + date_delta:
                dates.append(date.strftime("%d-%m"))
                date += date_delta
            marks = MarkSerializer(marks,many=True).data
            grade_subjects= GradeSubjectSerializer(grade_subjects,many=True).data
            content = {'marks':marks, 'grade_subjects':grade_subjects,'dates': dates}
            return Response(content,status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @list_route(methods=['get'])
    def teacher_table_data(self,request):
        #TODO make this
        pass
    def student_check(self, user):
        return not user.is_anonymous and user.staff == 'S'

    def teacher_check(self, user):
        return not user.is_anonymous and user.staff == 'T'
