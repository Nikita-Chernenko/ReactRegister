from rest_framework import serializers

from marks.models import Mark, GradeSubject, Subject, Student


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"
        depth = 1


class GradeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSubject
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
