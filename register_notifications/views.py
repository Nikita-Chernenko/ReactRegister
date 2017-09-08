from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from register_notifications.models import RegisterNotification
from register_notifications.serializers import RegisterNotificationSerializer


class RegisterNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterNotificationSerializer
    queryset = RegisterNotification.objects.all()

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