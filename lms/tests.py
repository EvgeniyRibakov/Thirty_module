from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='User1_Python2025')
        self.user2 = User.objects.create_user(username='user2', password='User2_Python2025')
        self.moderator = User.objects.create_user(username='moderator', password='Moderator2025')
        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator.groups.add(self.moderator_group)
        self.course = Course.objects.create(title='Test Course', description='Test Desc', owner=self.user1)
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description

            ='Test Desc',
            course=self.course,
            owner=self.user1,
            video_link='https://youtube.com/watch?v=abc123'
        )

    def test_create_lesson_unauthenticated(self):
        response = self.client.post('/api/lessons/', {
            'title': 'New Lesson',
            'description': 'New Desc',
            'course': self.course.id,
            'video_link': 'https://youtube.com/watch?v=def456'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/lessons/', {
            'title': 'New Lesson',
            'description': 'New Desc',
            'course': self.course.id,
            'video_link': 'https://youtube.com/watch?v=def456'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_invalid_link(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/lessons/', {
            'title': 'New Lesson',
            'description': 'New Desc',
            'course': self.course.id,
            'video_link': 'https://example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', {
            'title': 'Updated Lesson'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_update_lesson_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', {
            'title': 'Updated Lesson'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', {
            'title': 'Updated Lesson'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_owner_separate_endpoint(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(f'/api/lessons/{self.lesson.id}/update/', {
            'title': 'Updated Lesson via UpdateView',
            'description': 'Test Desc',
            'course': self.course.id,
            'owner': self.user1.id,
            'video_link': 'https://youtube.com/watch?v=abc123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson via UpdateView')

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_owner_separate_endpoint(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='User1_Python2025')
        self.course = Course.objects.create(title='Test Course', description='Test Desc', owner=self.user)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_unauthenticated(self):
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
