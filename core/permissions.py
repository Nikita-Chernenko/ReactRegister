from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.staff == 'T'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff == 'S'
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff == 'T'