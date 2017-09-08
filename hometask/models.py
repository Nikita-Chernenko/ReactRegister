from django.db import models
from timetable.models import ScheduledSubject


class Hometask(ScheduledSubject):
    task = models.CharField(max_length=200)
    files = models.FileField(upload_to="uploads/",null=True)
