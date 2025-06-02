from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class IsAuthenticatedCustom(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        return True


# Заглушки для сериализаторов, замените на ваши
class UserSerializer:
    def __init__(self, instance=None, data=None, many=False, partial=False):
        self.instance = instance
        self.data = data if data else (instance if instance else {})
        self.many = many
        self.partial = partial

    def is_valid(self):
        return True

    def save(self, **kwargs):
        user = self.instance or get_user_model().objects.create(**self.data)
        for key, value in self.data.items():
            setattr(user, key, value)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        self.instance = user
        return user


class PaymentSerializer:
    def __init__(self, instance=None, data=None, many=False, partial=False):
        self.instance = instance
        self.data = data if data else (instance if instance else {})
        self.many = many
        self.partial = partial

    def is_valid(self):
        return True

    def save(self, **kwargs):
        return self.instance or {'id': 1, 'user': kwargs.get('user')}


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def list(self, request):
        users = self.queryset
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = PaymentSerializer
    queryset = []  # Замените на ваш queryset

    def list(self, request):
        payments = self.queryset
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    def update(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.get_serializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.get_serializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        payment = get_object_or_404(self.queryset, pk=pk, user=request.user)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentStripeCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        return Response({"message": "Stripe payment created"}, status=status.HTTP_201_CREATED)