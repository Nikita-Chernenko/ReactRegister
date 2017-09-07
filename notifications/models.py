from django.db import models

from marks.models import Teacher, Student
from timetable.models import ScheduledSubject


class RegisterNotification(ScheduledSubject):
    sender = models.ForeignKey(Teacher)
    receiver = models.ForeignKey(Student)
    value = models.CharField(max_length=10)
    def __str__(self):
        if self.value == "н":
            return "Вам был поставлен пропуск в связи с отсутствием " + self.date.strftime("%d/%m")  +\
                   " На предмете " +  str(self.grade_subject)
        else:
            return self.sender.surname + " " + self.sender.name +\
               " поставил/а: " + str(self.value) + " По предмету " + str(self.grade_subject) + \
               " За " + self.date.strftime("%d/%m")
