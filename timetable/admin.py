from django.contrib import admin
from timetable.models import ScheduledSubject, ClassTime


@admin.register(ScheduledSubject, ClassTime)
class TimetableAdmin(admin.ModelAdmin):
    pass