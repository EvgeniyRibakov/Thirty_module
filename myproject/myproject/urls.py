from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from lms.views import CourseViewSet, LessonListCreateView, LessonDetailView, LessonUpdateView, LessonDeleteView, SubscriptionView
from users.views import PaymentViewSet, UserViewSet, PaymentStripeCreateAPIView  # Добавляем для Stripe
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def home(request):
    return HttpResponse("Welcome to the LMS API! Visit /api/ for available endpoints or /admin/ for the admin panel.")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/courses/', CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-list'),
    path('api/courses/<int:pk>/', CourseViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='course-detail'),
    path('api/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('api/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('api/lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('api/lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
    path('api/subscriptions/', SubscriptionView.as_view(), name='subscription-manage'),
    path('api/payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-list'),
    path('api/payments/<int:pk>/', PaymentViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='payment-detail'),
    path('api/payments/stripe/', PaymentStripeCreateAPIView.as_view(), name='payment-stripe-create'),
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('api/users/<int:pk>/', UserViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='user-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)