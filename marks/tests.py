from datetime import datetime, time

from annoying.functions import get_object_or_None
from django.test import TestCase

from absence.models import Absence
from classtime.models import ClassTime
from classtime.views import ClassTimeViewSet
from marks.models import Teacher, Student, GradeSubject
from register_notifications.models import RegisterNotification
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, RequestsClient, APIClient

from core.models import User
from marks.views import MarkViewSet
from marks.models import Mark
from timetable.models import ScheduledSubject


class MarkTest(TestCase):
    # def make_test(self):
    #     self.test_student_api()
    #     self.test_teacher_api()
    fixtures = ['all.json']

    def test_student_api(self):
        factory = APIRequestFactory()
        student_user = User.objects.get(username='student1')
        self.student_list_api(factory, student_user)
        self.student_detail_api(factory, student_user)

    def student_list_api(self, factory, student_user):
        # post methods are not allowed to student
        mark_list = MarkViewSet.as_view({'get': 'list', 'post': 'create'})
        student_request = factory.post('/api/v0/marks', {'value': 10, 'student_id': 1,
                                                         'date': '2017-11-10', 'grade_subject_id': 1,
                                                         'class_time_id': 1})
        force_authenticate(student_request, student_user, student_user.auth_token)
        response = mark_list(student_request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        notification = get_object_or_None(RegisterNotification, receiver=Student(student_user=student_user),
                                          date=datetime(2017, 11, 10).date(),
                                          grade_subject_id=1, class_time_id=1)
        self.assertIsNone(notification)

        # testing that returning objects belong to student
        student_request = factory.get('/api/v0/marks')
        force_authenticate(student_request, student_user, student_user.auth_token)
        response = mark_list(student_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        marks = Mark.objects.filter(student=Student.objects.get(student_user=student_user))
        self.assertEqual(len(response.data), len(marks))

        # testing filters
        student_request = factory.get('api/v0/marks?lesson_start__gte=10:15:00&'
                                      'lesson_end__lte=15:00:00&date__gte=2017-09-05&'
                                      'date__lte=2017-09-27')
        force_authenticate(student_request, student_user, student_user.auth_token)
        response = mark_list(student_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        marks = Mark.objects.filter(student=Student.objects.get(student_user=student_user)). \
            filter(class_time__lesson_start__gte=time(10, 15), class_time__lesson_end__lte=time(15),
                   date__gte=datetime(2017, 9, 5).date(), date__lte=datetime(2017, 9, 27).date())
        self.assertEqual(len(response.data), len(marks))

        # testing student table
        client = APIClient()
        client.force_authenticate(user=student_user,token=student_user.auth_token)
        response = client.get('/api/v0/marks/student_table_data/?date_from=2017-09-05&date_to=2017-09-08')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['marks'][0]['date'], '2017-09-05')
        self.assertEqual(response.data['marks'][-1]['date'],'2017-09-08')
        self.assertEqual(response.data['dates'][0],'05-09')
        self.assertEqual(response.data['dates'][-1],'08-09')
        self.assertEqual(response.data['marks'][0]['grade_subject'],204)
        self.assertEqual(response.data['marks'][-1]['grade_subject'],204)

    def student_detail_api(self, factory, student_user):
        marks_list = MarkViewSet.as_view({'get':'retrieve'})
        student_requset = factory.get('/api/v0/marks')
        force_authenticate(student_requset, student_user, student_user.auth_token)
        response = marks_list(student_requset,
                              pk=Mark.objects.filter(student=Student.objects.get(student_user=student_user)).first().id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_api(self):
        factory = APIRequestFactory()
        teacher_user = User.objects.get(username='teacher1')
        self.teacher_list_api(factory, teacher_user)
        self.teacher_detail_api(factory, teacher_user)

    def teacher_list_api(self, factory, teacher_user):
        # creating mark and notification so
        mark_list = MarkViewSet.as_view({'get': 'list', 'post': 'create'})
        scheduled_subject = ScheduledSubject(class_time=ClassTime.objects.last(),
                                             grade_subject=GradeSubject.objects.filter(
                                                 teacher__teacher_user=teacher_user).last(),
                                             date=datetime(2017, 11, 11).date())
        teacher_request = factory.post('api/v0/marks',
                                       {'value': 10,
                                        'student': scheduled_subject.grade_subject.grade.student_set.last().id,
                                        'date': scheduled_subject.date,
                                        'grade_subject': scheduled_subject.grade_subject.id,
                                        'class_time': scheduled_subject.class_time.id}, format='json')

        force_authenticate(teacher_request, teacher_user, teacher_user.auth_token)
        response = mark_list(teacher_request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        notification = get_object_or_None(RegisterNotification,
                                          receiver_id=scheduled_subject.grade_subject.grade.student_set.last().id,
                                          sender=Teacher.objects.get(teacher_user=teacher_user),
                                          date=scheduled_subject.date,
                                          grade_subject_id=scheduled_subject.grade_subject.id,
                                          class_time_id=scheduled_subject.class_time.id)
        self.assertIsNotNone(notification)

        # Testing destroying absence while crating it in the same day as mark
        absence = Absence(value='f', student=Student.objects.first(), date=datetime(2017, 11, 11).date(),
                          grade_subject=GradeSubject.objects.first(), class_time=ClassTime.objects.first())
        absence.save()

        Mark(value='10', student=Student.objects.first(), date=datetime(2017, 11, 11).date(),
             grade_subject=GradeSubject.objects.first(), class_time=ClassTime.objects.first()).save()
        Mark(value='11', student=Student.objects.first(), date=datetime(2017, 11, 11).date(),
             grade_subject=GradeSubject.objects.first(), class_time=ClassTime.objects.first()).save()
        absence = get_object_or_None(Absence, student=Student.objects.first(), date=datetime(2017, 11, 11).date(),
                                     grade_subject=GradeSubject.objects.first(), class_time=ClassTime.objects.first())
        self.assertIsNone(absence)
        self.assertEqual(len(Mark.objects.filter(student=Student.objects.first(), date=datetime(2017, 11, 11).date(),
                                                 grade_subject=GradeSubject.objects.first(),
                                                 class_time=ClassTime.objects.first())), 2)
        Mark.objects.last().delete()
        Mark.objects.last().delete()

        # testing that returning objects belong to teacher
        mark_list = MarkViewSet.as_view({'get': 'list'})
        teacher_request = factory.get('api/v0/marks')
        force_authenticate(teacher_request, teacher_user, teacher_user.auth_token)
        response = mark_list(teacher_request)
        marks = Mark.objects.filter(grade_subject__teacher__teacher_user=teacher_user)
        self.assertEqual(len(response.data), len(marks))

        # testing filters
        teacher_request = factory.get('api/v0/marks?lesson_start__gte=10:15:00&'
                                      'lesson_end__lte=15:00:00&date__gte=2017-09-05&'
                                      'date__lte=2017-09-27')
        force_authenticate(teacher_request, teacher_user, teacher_user.auth_token)
        response = mark_list(teacher_request)
        marks = Mark.objects.filter(class_time__lesson_start__gte=time(10, 15), class_time__lesson_end__lte=time(15),
                                    date__gte=datetime(2017, 9, 5).date(), date__lte=datetime(2017, 9, 27).date()). \
            filter(grade_subject__teacher__teacher_user=teacher_user)

        self.assertEqual(len(response.data), len(marks))

        #testing teacher table
        # testing student table
        client = APIClient()
        client.force_authenticate(user=teacher_user, token=teacher_user.auth_token)
        grade_subject_id = GradeSubject.objects.filter(teacher__teacher_user=teacher_user).last().id
        response = client.get('/api/v0/marks/teacher_table_data/?date_from=2017-09-06&date_to=2017-09-08&grade_subject_id='+
                              str(grade_subject_id))
        grade=GradeSubject.objects.get(pk=grade_subject_id).grade
        students =Student.objects.filter(grade=grade)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['marks'][0]['date'], '2017-09-06')
        self.assertEqual(response.data['marks'][-1]['date'], '2017-09-08')
        self.assertEqual(response.data['dates'][0], datetime(2017,9,6).strftime('%d-%m %a'))
        self.assertEqual(response.data['dates'][-1], datetime(2017,9,8).strftime('%d-%m %a'))
        self.assertEqual(response.data['marks'][0]['grade_subject'], grade_subject_id)
        self.assertEqual(response.data['marks'][-1]['grade_subject'], grade_subject_id)
        self.assertEqual(response.data['students'][0]['id'],students.first().id)
        self.assertEqual(response.data['students'][-1]['id'],students.last().id)
        # for mark in response.data['marks']:
        #     print(str(mark['student']) + " " + str(mark['date'] + ' ' + str(mark['grade_subject'])))
    def teacher_detail_api(self, factory, teacher_user):
        # updating mark_list and changing notification so
        scheduled_subject = ScheduledSubject(class_time=ClassTime.objects.last(),
                                             grade_subject=GradeSubject.objects.filter(
                                                 teacher__teacher_user=teacher_user).last(),
                                             date=datetime(2017, 11, 11).date())
        mark_list = MarkViewSet.as_view({'post': 'update'})
        teacher_request = factory.post('api/v0/marks',
                                       {'value': 11,
                                        'student': scheduled_subject.grade_subject.grade.student_set.last().id,
                                        'date': scheduled_subject.date,
                                        'grade_subject': scheduled_subject.grade_subject.id,
                                        'class_time': scheduled_subject.class_time.id}, format='json')
        force_authenticate(teacher_request, teacher_user, teacher_user.auth_token)
        response = mark_list(teacher_request, pk=Mark.objects.last().id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 11)
        notification = get_object_or_None(RegisterNotification,
                                          receiver_id=scheduled_subject.grade_subject.grade.student_set.last().id,
                                          sender=Teacher.objects.get(teacher_user=teacher_user),
                                          date=scheduled_subject.date,
                                          grade_subject_id=scheduled_subject.grade_subject.id,
                                          class_time_id=scheduled_subject.class_time.id)
        self.assertEqual(int(notification.value), 11)
