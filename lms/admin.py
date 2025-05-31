from django.contrib import admin
from .models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']
    list_filter = ['owner']
    search_fields = ['title']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'video_url', 'owner']
    list_filter = ['course', 'owner']
    search_fields = ['title']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['course', 'user']
    search_fields = ['user__username', 'course__title']
