from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from .serializers import *


class CustomTokenCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenCreateSerializer

    @extend_schema(
        summary="Вход",
        description="Получение токена для аутентификации",
        responses={
            status.HTTP_200_OK: serializer_class(),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name="BadRequestResponse",
                fields={"detail": serializers.CharField(default="Неверный запрос")}
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name="UnauthorizedResponse",
                fields={"detail": serializers.CharField(default="Неавторизованный доступ")}
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name="ForbiddenResponse",
                fields={"detail": serializers.CharField(default="Доступ запрещен")}
            ),
        },
        tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key})


class CustomTokenDestroyView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Выход",
        description="Удаление токена",
        request=None,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name="Logout",
                fields={"detail": serializers.CharField(default="Выход из системы успешен")}
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name="BadRequestResponse",
                fields={"detail": serializers.CharField(default="Неверный запрос")}
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name="UnauthorizedResponse",
                fields={"detail": serializers.CharField(default="Неавторизованный доступ")}
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name="ForbiddenResponse",
                fields={"detail": serializers.CharField(default="Доступ запрещен")}
            ),
        },
        tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(status=204)
        except Token.DoesNotExist:
            return Response(status=400, data={'detail': 'Invalid token or user not authenticated.'})


class UserInfoView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Получение данных пользователя",
        description="Получение данных авторизованного пользователя",
        responses={
            status.HTTP_200_OK: CustomUserSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name="BadRequest",
                fields={"detail": serializers.CharField(default="Неверный запрос")}
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name="UnauthorizedResponse",
                fields={"detail": serializers.CharField(default="Неавторизованный доступ")}
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name="ForbiddenResponse",
                fields={"detail": serializers.CharField(default="Доступ запрещен")}
            ),
        },
        tags=["users"]
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Обновление данных пользователя",
        description="Обновление данных авторизованного пользователя",
        request=UserPatchSerializer,
        responses={
            status.HTTP_200_OK: UserPatchSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name="BadRequestResponse",
                fields={"detail": serializers.CharField(default="Неверный запрос")}
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name="UnauthorizedResponse",
                fields={"detail": serializers.CharField(default="Неавторизованный доступ")}
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name="ForbiddenResponse",
                fields={"detail": serializers.CharField(default="Доступ запрещен")}
            ),
        },
        tags=["users"]
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        users = CustomUser.objects.get(id=user.id)
        serializer = UserPatchSerializer(
            instance=users, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
