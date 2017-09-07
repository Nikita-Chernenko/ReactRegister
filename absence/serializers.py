
from rest_framework import serializers

from absence.models import Absence



class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = '__all__'