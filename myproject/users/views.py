from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from lms.models import Course
import stripe
from django.conf import settings
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    @extend_schema(
        summary="Список пользователей",
        description="Возвращает список всех пользователей. Доступно только авторизованным пользователям.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание пользователя",
        description="Создает нового пользователя (регистрация). Доступно всем.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение пользователя",
        description="Возвращает информацию о пользователе по ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление пользователя",
        description="Обновляет данные пользователя по ID.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление пользователя",
        description="Частично обновляет данные пользователя по ID.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя по ID.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']

    @extend_schema(
        summary="Список платежей",
        description="Возвращает список всех платежей с фильтрацией и сортировкой.",
        parameters=[
            OpenApiParameter(name='course', description='ID курса для фильтрации', required=False, type=int),
            OpenApiParameter(name='lesson', description='ID урока для фильтрации', required=False, type=int),
            OpenApiParameter(name='payment_method', description='Метод оплаты для фильтрации', required=False,
                             type=str),
            OpenApiParameter(name='ordering', description='Сортировка по дате платежа', required=False, type=str),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание платежа",
        description="Создает новый платеж. Для оплаты через Stripe используйте /api/payments/stripe/.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение платежа",
        description="Возвращает информацию о платеже по ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление платежа",
        description="Обновляет данные платежа по ID.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление платежа",
        description="Частично обновляет данные платежа по ID.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление платежа",
        description="Удаляет платеж по ID.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


def create_stripe_product(course: Course) -> str:
    """Создает продукт в Stripe на основе курса."""
    product = stripe.Product.create(
        name=course.title,
        description=course.description or "No description",
    )
    return product.id


def create_stripe_price(product_id: str, amount: float) -> str:
    """Создает цену для продукта в Stripe (в копейках)."""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # Переводим в копейки
        currency="usd",
        product=product_id,
    )
    return price.id


def create_stripe_checkout_session(price_id: str, course_id: int) -> tuple:
    """Создает сессию оплаты в Stripe и возвращает ID сессии и URL."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        metadata={"course_id": course_id},
    )
    return session.id, session.url


class PaymentStripeCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Создание платежа через Stripe",
        description="Создает платеж для курса через Stripe и возвращает ссылку на оплату.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "course": {"type": "integer", "description": "ID курса"},
                    "amount": {"type": "number", "description": "Сумма платежа"},
                },
                "required": ["course", "amount"],
            }
        },
        responses={
            201: {
                "type": "object",
                "properties": {
                    "payment_id": {"type": "integer"},
                    "stripe_payment_url": {"type": "string"},
                },
            }
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        amount = request.data.get("amount")

        if not course_id or not amount:
            return Response({"error": "Course ID and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            product_id = create_stripe_product(course)
            price_id = create_stripe_price(product_id, float(amount))
            session_id, payment_url = create_stripe_checkout_session(price_id, course_id)

            payment = Payment.objects.create(
                user=user,
                course=course,
                amount=amount,
                payment_method=Payment.PaymentMethod.STRIPE,
                stripe_session_id=session_id,
                stripe_payment_url=payment_url,
            )

            return Response({
                "payment_id": payment.id,
                "stripe_payment_url": payment.stripe_payment_url,
            }, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
