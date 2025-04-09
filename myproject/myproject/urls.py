from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myproject.lms.views import CourseViewSet, LessonListCreateView, LessonDetailView, LessonUpdateView, \
    LessonDeleteView
from myproject.users.views import PaymentViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include(router.urls)),
                  path('api/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
                  path('api/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
                  path('api/lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
                  path('api/lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
