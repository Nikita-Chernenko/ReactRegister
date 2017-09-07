from django.db import models
from timetable.models import ScheduledSubject


class HomeTask(ScheduledSubject):
    task = models.CharField(max_length=200)
