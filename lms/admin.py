from django.contrib import admin
from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'video_link', 'owner', 'created_at']  # Заменили video_url на video_link
    list_filter = ['created_at', 'course']
    search_fields = ['title', 'description']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'course__title']
