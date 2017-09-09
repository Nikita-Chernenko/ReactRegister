import datetime

from annoying.functions import get_object_or_None
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from classtime.models import ClassTime
from core.permissions import IsTeacherOrReadOnly
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
        try:
            staff = user.staff
        except:
            staff = None
        if staff == "S":
            queryset = queryset.filter(student=Student.objects.get(student_user=user)).order_by('date',
                                                                                                'class_time__lesson_start')
        elif staff == "T":
            grade_subject_id = self.request.query_params.get("grade_subject_id", None)
            queryset = queryset.filter(grade_subject_id=grade_subject_id)
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user
        value = request.data['value']
        student = request.data['student']
        class_time_id = request.data['class_time']
        date = request.data['date']
        grade_subject_id = request.data['grade_subject']
        RegisterNotification(sender=Teacher.objects.get(teacher_user=user), reciever=student, value=value,
                             class_time=ClassTime.objects.get(pk=class_time_id),
                             date=date, grade_subject=GradeSubject.objects.get(pk=grade_subject_id)).save()
        return super(self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        value = request.data['value']
        user = self.request.user
        student = request.data['student']
        class_time = request.data['class_time']
        date = request.data['date']
        grade_subject = request.data['grade_subject']
        notification = RegisterNotification.objects.get(sender=user, reciever=student,
                                                        class_time=class_time, date=date, grade_subject=grade_subject)
        notification.value = value
        notification.save()
        return super(self).update(request, *args, **kwargs)

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

    # student token = "Authorization: Token 473cd764e73faf62f185b65e05a655eb9323259f"
    @list_route(methods=['get'])
    def student_table_data(self, request):
        user = self.request.user
        if self.student_check(user=user):
            try:
                date_from, date_to = self.get_query_dates()
            except:
                content = {'bad date': 'date_from:"01.10.2017", date_to:"30.10.2017"'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            marks = Mark.objects.filter(student=Student.objects.get(student_user=user)). \
                order_by('date', 'class_time__lesson_start')
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
        if self.teacher_check(user):
            grade_subject_id = self.request.query_params.get('grade_subject_id', 0)
            date_from, date_to = self.get_query_dates()
            if grade_subject_id is None:
                return Response({'no correct grade_subject_id'}, status=status.HTTP_400_BAD_REQUEST)
            all_marks = Mark.objects.order_by('date').filter(grade_subject_id=grade_subject_id). \
                filter(date__gte=date_from).filter(date__lte=date_to)
            grade = get_object_or_None(Grade, gradesubject__id=grade_subject_id)
            dates = [sub for sub in ScheduledSubject.objects.
                filter(grade_subject_id=grade_subject_id).filter(date__gt=date_from).
                filter(date__lt=date_to).values_list('date', flat=True).distinct()]
            students = Student.objects.filter(grade=grade)
            marks = MarkSerializer(all_marks, many=True).data
            students = StudentSerializer(students, many=True).data
            return Response({'marks': marks, 'students': students, 'dates': dates})

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_query_dates(self):
        date_from = datetime.datetime.strptime(self.request.query_params.get("data_from", "8.09.2017").strip(),
                                               "%d.%m.%Y").date()
        date_to = datetime.datetime.strptime(self.request.query_params.get("data_to", "12.09.2017").strip(),
                                             "%d.%m.%Y").date()
        return date_from, date_to

    def student_check(self, user):
        return not user.is_anonymous and user.staff == 'S'

    def teacher_check(self, user):
        return not user.is_anonymous and user.staff == 'T'
