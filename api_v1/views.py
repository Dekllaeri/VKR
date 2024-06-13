from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from drf_spectacular.utils import extend_schema, inline_serializer

from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import *


class LastNewsView(generics.GenericAPIView):
    """
    Представление для возврата последней новости
    """

    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Последняя опубликованная новость",
        description="Получение последней опубликованной новости",
        responses={
            status.HTTP_200_OK: serializer_class(),
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
        tags=["news"]
    )
    def get(self, request):
        news = News.objects.filter(status=2).order_by('-updated_at').first()

        serializer = self.serializer_class(news, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateRequestView(generics.GenericAPIView):
    """
    Представление для создания заявки
    """

    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Создание заявки",
        description="Создание новой заявки.",
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
        tags=["request"]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, status=1)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class RequesrListView(generics.GenericAPIView):
    """
    Представление для возврата всех заявок
    """

    serializer_class = RequestListSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Получение списка не закрытых заявок",
        description="Получение списка не закрытых заявок",
        responses={
            status.HTTP_200_OK: serializer_class(many=True),
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
        tags=["request"]
    )
    def get(self, request):
        requests = Request.objects.filter(~Q(status=3))

        serializer = self.serializer_class(requests, context={'request': request}, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RequestSetStatusView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = RequestPatchSerializer

    @extend_schema(
        summary="Изменение статуса заявки",
        description="Изменение статуса заявки",
        request=serializer_class,
        responses={
            status.HTTP_200_OK: serializer_class,
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
        tags=["request"]
    )
    def patch(self, request, id, *args, **kwargs):
        try:
            requests = Request.objects.get(id=id)
        except Request.DoesNotExist:
            return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=requests, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class NewsCreateView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = NewsCreateSerializer

    @extend_schema(
        summary="Создание новости",
        description="Создание новой новости, создаётся как черновик.",
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
        tags=["news"]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=1)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class NewsUpdateView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = NewsPatchSerializer

    @extend_schema(
        summary="Изменение новости",
        description="Изменение новости",
        request=serializer_class,
        responses={
            status.HTTP_200_OK: serializer_class,
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
        tags=["news"]
    )
    def patch(self, request, id, *args, **kwargs):
        try:
            news = News.objects.get(id=id)
        except News.DoesNotExist:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=news, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
