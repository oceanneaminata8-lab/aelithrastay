from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class IsHostOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.role in ('host', 'admin'))
        )


class IsPropertyHostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.host_id == request.user.id


class IsBookingParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or obj.guest_id == request.user.id
            or obj.property.host_id == request.user.id
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'user', None) or getattr(obj, 'guest', None)
        return request.user.is_staff or owner == request.user
