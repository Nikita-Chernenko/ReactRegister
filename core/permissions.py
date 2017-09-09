from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print (request.method)
        print (request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        print(request.user.staff)
        return request.user.staff == 'T'