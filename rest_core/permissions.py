from django.contrib.auth.models import User
from rest_framework import permissions


class IsDriver(permissions.BasePermission):
    """
    This class prohibits accesses for all users
    except drivers.
    """

    def has_permission(self, request, view):
        if not request.user.profile.driver:
            return False
        return True


class IsOwner(permissions.BasePermission):
    """
    This class restricts accesses to resources only
    for their owners or superuser.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        user_pk = view.kwargs.get('user_pk', None)
        pk = view.kwargs.get('pk', None)

        user_pk = user_pk if user_pk else pk
        if user_pk:
            user = User.objects.get(pk=user_pk)
            if request.user == user:
                return True
        return False
