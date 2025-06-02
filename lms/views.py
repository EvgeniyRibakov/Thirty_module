from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from django.shortcuts import get_object_or_404
from lms.models import Lesson, Course, Subscription
from lms.serializers import LessonSerializer, SubscriptionSerializer, CourseSerializer


class IsAuthenticatedCustom(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        return True


class CourseViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def list(self, request):
        courses = self.queryset.filter(owner=request.user)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.get_serializer(course)
        return Response(serializer.data)

    def update(self, request, pk=None):
        course = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.get_serializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        course = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        course = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonListCreateView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        lessons = Lesson.objects.filter(owner=request.user)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonUpdateView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def put(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDeleteView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        serializer = SubscriptionSerializer(data={'user': request.user.id, 'course': request.data.get('course')})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id):
        subscription = get_object_or_404(Subscription, user=request.user, course_id=course_id)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)