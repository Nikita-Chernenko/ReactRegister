from rest_framework import serializers
from classtime.models import ClassTime


class ClassTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTime
        fields = ('id', 'lesson_start', 'lesson_end')
