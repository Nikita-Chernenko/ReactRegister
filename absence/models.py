from annoying.functions import get_object_or_None
from django.db import models

from marks.models import Student
from timetable.models import ScheduledSubject


class Absence(ScheduledSubject):
    value = models.CharField(verbose_name='absence',max_length=1,default='н')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    unique_together = (("class_time", "date"),)

    def save(self, *args, **kwargs):
        from marks.models import Mark
        mark = Mark.objects.filter(student=self.student, grade_subject=self.grade_subject,
                                         class_time=self.class_time, date=self.date)
        mark.delete()
        self.value = 'н'
        super(Absence, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.student) + " " + str(self.grade_subject_id) + str(self.date) + str(self.class_time_id)
