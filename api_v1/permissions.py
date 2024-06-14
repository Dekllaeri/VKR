from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
# AllowAny и IsAuthenticated импортируются для использования их при импорте данного файла.


class IsAdmin(BasePermission):
    """
    Право доступа имею те авторизованные пользователи, у которых поле is_admin=True или is_superuser=True
    (являются персоналом: администраторы и суперпользователи)
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_admin or request.user.is_superuser))


class IsClient(BasePermission):
    """
    Право доступа имею те авторизованные пользователи, у которых поле is_client=True
    (являются клиентами)
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_client)
