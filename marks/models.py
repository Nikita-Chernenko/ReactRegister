import django_filters
from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.db import models

from DjangoReact import settings


class Subject(models.Model):
    short_name = models.CharField(max_length=6, default="")
    full_name = models.CharField(max_length=20, default="")

    def __str__(self):
        return str(self.full_name)


class Teacher(models.Model):
    teacher_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    self_classroom = models.CharField(max_length=6)

    def __str__(self):
        return self.name + " " + self.surname


class Grade(models.Model):
    grade_number = models.CharField(max_length=5)
    head_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Class № " + str(self.grade_number)
        # + " Head: "  + str(self.head_teacher )


        # def __str__(self):
        #     return str(self.grade_number)


class GradeSubject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    classroom = models.CharField(max_length=5)

    def __str__(self):
        return str(self.subject) + ' ' + str(self.grade) + " " + str(self.teacher)

        # def __str__(self):
        #     return str(self.subject) + " " + str(self.grade)


class Student(models.Model):
    student_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.surname + " " + str(self.grade)
        # def __str__(self):
        #     return self.name + " " + self.surname



from timetable.models import  ScheduledSubject
class Mark(ScheduledSubject):
    value = models.IntegerField(verbose_name="mark")
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    def save(self,*args,**kwargs):
        from absence.models import Absence
        absence= get_object_or_None(Absence,student = self.student, grade_subject = self.grade_subject,
                                    class_time_id = self.class_time_id,date = self.date)
        if absence is not None:
            absence.delete()
        super(Mark,self).save(*args,**kwargs)
    def __str__(self):
        return " Value " + str(self.value) + " " + str(self.student) + \
               " Subject " ' '+str( self.grade_subject.subject) + " Date " + str(self.date.strftime("%d/%m/%Y"))
        # def __str__(self):
        #     return " Mark is : " + self.value.__str__() + " Date is: " + self.date.strftime("%d/%m/%Y")

