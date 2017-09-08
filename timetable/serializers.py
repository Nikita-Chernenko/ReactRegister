from rest_framework import serializers

from timetable.filters import ScheduledSubjectFilter
from timetable.models import ScheduledSubject


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledSubject
        fields = '__all__'