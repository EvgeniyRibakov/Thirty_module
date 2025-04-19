from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_link


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_youtube_link], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
