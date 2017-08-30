from django.db import models

from marks.models import Student
from timetable.models import ScheduledSubject


class Absence(ScheduledSubject):
    value = models.CharField(verbose_name='absence',max_length=1,default='н')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    unique_together = (("class_time", "date"),)

    def save(self, *args, **kwargs):
        self.value = 'н'
        super(Absence, self).save(*args, **kwargs)
