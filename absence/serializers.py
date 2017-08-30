from rest_framework import serializers

from absence.models import Absence



class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ('id', 'date','lesson_start','lesson_end', 'grade_subject', 'value','student')