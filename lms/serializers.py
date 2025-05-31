from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_link


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_youtube_link], required=False, allow_blank=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)  # Делаем owner только для чтения

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
