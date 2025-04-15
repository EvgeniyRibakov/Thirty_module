# myproject/myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet, LessonListCreateView, LessonDetailView, LessonUpdateView, LessonDeleteView
from users.views import PaymentViewSet, UserViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'users', UserViewSet)


# Простая функция для корневого URL
def home(request):
    return HttpResponse("Welcome to the LMS API! Visit /api/ for available endpoints or /admin/ for the admin panel.")


urlpatterns = [
                  path('', home, name='home'),
                  path('admin/', admin.site.urls),
                  path('api/', include(router.urls)),
                  path('api/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
                  path('api/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
                  path('api/lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
                  path('api/lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
