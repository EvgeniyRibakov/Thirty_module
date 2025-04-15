# myproject/users/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:  # Регистрация доступна всем
            self.permission_classes = [AllowAny]
        else:  # Остальные действия (list, retrieve, update, destroy) только для авторизованных
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']
