#from rest_framework.permissions import BasePermission
#
#
# class IsPostAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and request.user == obj.author
#
#
from rest_framework.permissions import BasePermission


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user