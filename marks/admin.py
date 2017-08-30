from django.contrib import admin
from marks.models import *
@admin.register(Student,Teacher,Subject,GradeSubject,Grade,Mark)
class MarkAdmin(admin.ModelAdmin):
    pass

