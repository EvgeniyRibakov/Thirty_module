# myproject/lms/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', null=True, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', null=True)  # Поле владельца

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lesson_previews/', null=True, blank=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', null=True)  # Поле владельца

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
