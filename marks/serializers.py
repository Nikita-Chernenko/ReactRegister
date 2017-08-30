from rest_framework import serializers

from marks.models import Mark, GradeSubject


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"

class GradeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        module = GradeSubject
        fields = "__all__"