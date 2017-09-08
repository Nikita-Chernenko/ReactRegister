from rest_framework import  serializers

from hometask.models import Hometask


class HometaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = '__all__'