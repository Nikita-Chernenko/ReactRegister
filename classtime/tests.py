import datetime

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

from classtime.models import ClassTime
from classtime.views import ClassTimeViewSet
from core.models import User


class ClassTimeTest(TestCase):
    def create_instances(self):
        lesson_start = datetime.time(8, 30)
        lesson_end = datetime.time(9, 15)
        for x in range(8):
            ClassTime(lesson_start=lesson_start, lesson_end=lesson_end).save()
            if lesson_end == datetime.time(12):
                lesson_end = (
                datetime.datetime.combine(datetime.date(1, 1, 1), lesson_end) + datetime.timedelta(minutes=65)).time()
                lesson_start = (
                datetime.datetime.combine(datetime.date(1, 1, 1), lesson_start) + datetime.timedelta(minutes=65)).time()
            else:
                lesson_end = (
                datetime.datetime.combine(datetime.date(1, 1, 1), lesson_end) + datetime.timedelta(minutes=55)).time()
                lesson_start = (
                datetime.datetime.combine(datetime.date(1, 1, 1), lesson_start) + datetime.timedelta(minutes=55)).time()

    def test_creating(self):
        self.create_instances()

        classes_begin = ClassTime.objects.all().first()
        classes_end = ClassTime.objects.all().last()
        self.assertEqual(classes_begin.lesson_start, datetime.time(8, 30))
        self.assertEqual(classes_end.lesson_end, datetime.time(15, 50))
    def test_student_API(self):
        factory = APIRequestFactory()
        User(username='student1',password='qwert1234',staff="S").save()
        student = User.objects.get(username='student1')

        Token.objects.create(user = student)

        class_time_list = ClassTimeViewSet.as_view({'get': 'list'})
        class_time_detail = ClassTimeViewSet.as_view({'get': 'list'})

        student_request = factory.get('/classtimes')
        response_unauthenticated = class_time_list(student_request)
        self.assertEqual(response_unauthenticated.status_code,status.HTTP_401_UNAUTHORIZED )
        force_authenticate(student_request,student,token=student.auth_token)
        response = class_time_list(student_request)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)

        teacher_reqset = factory.get('')
    def test_teacher_API(self):
        factory = APIRequestFactory()

        User(username='teacher1', password='qwert1234', staff="T").save()
        teacher = User.objects.get(username='teacher1')
        Token.objects.create(user = teacher)

        class_time_list = ClassTimeViewSet.as_view({'get': 'list'})
        class_time_detail = ClassTimeViewSet.as_view({'get': 'list'})

        teacher_request = factory.get('/classtimes')
        response_unauthenticated = class_time_list(teacher_request)
        self.assertEqual(response_unauthenticated.status_code, status.HTTP_401_UNAUTHORIZED)

        force_authenticate(teacher_request, teacher, token=teacher.auth_token)
        response = class_time_list(teacher_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)
