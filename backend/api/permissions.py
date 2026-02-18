from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow staff members to edit objects.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated and has 'STAFF' or 'ADMIN' role or is a superuser
        return bool(request.user and request.user.is_authenticated and (
            request.user.role in ['STAFF', 'ADMIN'] or request.user.is_staff
        ))

class IsAdminOrStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow admin or staff members to edit objects.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (
            request.user.role in ['ADMIN', 'STAFF'] or request.user.is_staff or request.user.is_superuser
        ))
