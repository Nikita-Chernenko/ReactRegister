from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.checks import student_check
from core.permissions import IsStudent
from register_notifications.models import RegisterNotification
from register_notifications.serializers import RegisterNotificationSerializer


class RegisterNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterNotificationSerializer
    queryset = RegisterNotification.objects.all()
    permission_classes = (IsAuthenticated,IsStudent)

    @list_route(methods=['delete'])
    def delete_last(self,request):
        try:
            value = int(self.request.query_params.get('number',10))
        except ValueError:
            return Response({'value':'Integer number'}, status=status.HTTP_400_BAD_REQUEST)
        self.get_queryset()[-value].delete()

    @list_route(methods=['delete'])
    def delete_all(self,request):
        self.get_queryset().delete()

    def get_queryset(self):
        queryset = RegisterNotification.objects.all()
        user = self.request.user
        if student_check(user):
            queryset = queryset.filter(receiver__student_user=user)
        return queryset