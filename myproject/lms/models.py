from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        permissions = [
            ("can_view_course", "Can view course"),
            ("can_edit_course", "Can edit course"),
            ("can_delete_course", "Can delete course"),
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    video_link = models.URLField(blank=True, null=True)

    class Meta:
        permissions = [
            ("can_view_lesson", "Can view lesson"),
            ("can_edit_lesson", "Can edit lesson"),
            ("can_delete_lesson", "Can delete lesson"),
        ]

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.course.title}"
