from register_notifications.models import RegisterNotification
from rest_framework import serializers

class RegisterNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterNotification
        fields = '__all__'