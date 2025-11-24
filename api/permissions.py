from rest_framework import permissions

class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsReviewAuthorOrReadyOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, object):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(object.user==request.user)
    

class IsCartAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        return bool(request.user==obj.user)