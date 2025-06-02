from rest_framework import serializers
from lms.models import Lesson, Subscription, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner']


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_link', 'course', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True},
            'course': {'required': True}
        }

    def update(self, instance, validated_data):
        validated_data.pop('course', None)
        return super().update(instance, validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course']
        extra_kwargs = {
            'user': {'read_only': True}
        }