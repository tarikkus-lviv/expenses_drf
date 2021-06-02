from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.isAdmin()


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.isAdmin():
            return True
        return obj.user == request.user


class IsCurrentUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        if request.method in permissions.SAFE_METHODS or request.user.isAdmin():
            return True
        return obj.id == request.user.id
