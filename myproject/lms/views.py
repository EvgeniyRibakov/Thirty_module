from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CoursePagination, LessonPagination
from users.permissions import IsModerator, IsOwner
from drf_spectacular.utils import extend_schema, OpenApiParameter


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        summary="Список курсов",
        description="Возвращает список всех курсов с пагинацией.",
        parameters=[
            OpenApiParameter(name='page', description='Номер страницы', required=False, type=int),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание курса",
        description="Создает новый курс. Доступно только авторизованным пользователям, не модераторам.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение курса",
        description="Возвращает информацию о курсе по ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление курса",
        description="Обновляет данные курса по ID. Доступно модераторам и владельцу.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление курса",
        description="Частично обновляет данные курса по ID. Доступно модераторам и владельцу.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление курса",
        description="Удаляет курс по ID. Доступно только владельцу.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        summary="Список уроков",
        description="Возвращает список всех уроков с пагинацией.",
        parameters=[
            OpenApiParameter(name='page', description='Номер страницы', required=False, type=int),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Создание урока",
        description="Создает новый урок. Доступно только авторизованным пользователям, не модераторам.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    @extend_schema(
        summary="Получение урока",
        description="Возвращает информацию об уроке по ID.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление урока",
        description="Обновляет данные урока по ID. Доступно модераторам и владельцу.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление урока",
        description="Частично обновляет данные урока по ID. Доступно модераторам и владельцу.",
    )
    def patch(self, request, *args, **kwargs):
        print("PATCH method called")
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление урока",
        description="Удаляет урок по ID. Доступно модераторам и владельцу.",
    )
    def delete(self, request, *args, **kwargs):
        print("DELETE method called")
        return super().delete(request, *args, **kwargs)


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    @extend_schema(
        summary="Обновление урока (альтернативный эндпоинт)",
        description="Обновляет данные урока по ID. Доступно модераторам и владельцу.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class LessonDeleteView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    @extend_schema(
        summary="Удаление урока (альтернативный эндпоинт)",
        description="Удаляет урок по ID. Доступно только владельцу.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Управление подпиской",
        description="Добавляет или удаляет подписку пользователя на курс.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "course_id": {"type": "integer", "description": "ID курса"},
                },
                "required": ["course_id"],
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
            }
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription.exists():
            subscription.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'
        return Response({"message": message})
