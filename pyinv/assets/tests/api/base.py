from django.contrib.auth.models import Permission, User


class PermissionsMixin:

    _permission: str

    def _get_permission(self) -> Permission:
        return Permission.objects.get(codename=self._permission)

    def _set_permission(self, user: User) -> None:
        user.user_permissions.add(self._get_permission())


class APITestCase(PermissionsMixin):
    pass
