from datetime import datetime

from django.db import models
from django.utils.timezone import now

from classtime.models import ClassTime
from marks.models import GradeSubject


class ScheduledSubject(models.Model):
    class_time = models.ForeignKey(ClassTime,verbose_name="class time",on_delete=models.CASCADE)
    date = models.DateField(verbose_name="subject date",default=datetime(2017,9,10))
    grade_subject = models.ForeignKey(GradeSubject)
    # def __str__(self):
    #     return "Класс " + str(self.grade_subject.grade.grade_number)+ " Предмет: " + str(self.grade_subject.subject) +\
    #            " Время " + str(self.time) +  " Дата " + self.day.strftime("%B/%d") + " День недели " + str(self.day.isoweekday())
    def __str__(self):
        return str(self.grade_subject.grade.grade_number) + " " + str(self.grade_subject.subject)
