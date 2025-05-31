from django.db import models
from django.core.validators import URLValidator
from users.models import User
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="", null=False)  # Добавляем default и null=False
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(default=timezone.now)  # Временно nullable
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    video_link = models.URLField(validators=[URLValidator()], blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Временно nullable
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(default=timezone.now)  # Временно nullable

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.course.title}"