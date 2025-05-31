from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from lms.models import Course, Lesson


class LessonTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='User1_Python2025'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@example.com',
            password='User2_Python2025'
        )
        self.client.force_login(self.user)
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            course=self.course,
            owner=self.user,
            video_link='https://example.com/video'
        )

    def test_create_lesson_authenticated(self):
        # Тест логики создания урока для аутентифицированного пользователя
        pass

    def test_create_lesson_unauthenticated(self):
        # Тест логики создания урока для неаутентифицированного пользователя
        self.client.logout()
        response = self.client.post('/api/lessons/', {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_link': 'https://example.com/newvideo'
        })
        self.assertEqual(response.status_code, 403)

    def test_create_lesson_invalid_link(self):
        # Тест логики создания урока с недействительной ссылкой
        response = self.client.post('/api/lessons/', {
            'title': 'Invalid Link Lesson',
            'description': 'Invalid Link Description',
            'course': self.course.id,
            'video_link': 'invalid-link'
        })
        self.assertEqual(response.status_code, 400)

    def test_update_lesson_owner(self):
        # Тест обновления урока владельцем
        response = self.client.put(f'/api/lessons/{self.lesson.id}/', {
            'title': 'Updated Lesson',
            'description': 'Updated Description',
            'video_link': 'https://example.com/updatedvideo'
        })
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_update_lesson_not_owner(self):
        # Тест обновления урока не владельцем
        self.client.force_login(self.user2)
        response = self.client.put(f'/api/lessons/{self.lesson.id}/', {
            'title': 'Unauthorized Update',
            'description': 'Unauthorized Description'
        })
        self.assertEqual(response.status_code, 403)

    def test_update_lesson_moderator(self):
        # Тест обновления урока модератором (если есть логика модерации)
        pass

    def test_delete_lesson_owner(self):
        # Тест удаления урока владельцем
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_not_owner(self):
        # Тест удаления урока не владельцем
        self.client.force_login(self.user2)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_owner_separate_endpoint(self):
        # Тест удаления урока через отдельный эндпоинт
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_update_lesson_owner_separate_endpoint(self):
        # Тест обновления урока через отдельный эндпоинт
        response = self.client.put(f'/api/lessons/{self.lesson.id}/update/', {
            'title': 'Updated Lesson SE',
            'description': 'Updated Description SE'
        })
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson SE')


class SubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='User1_Python2025'
        )
        self.client.force_login(self.user)
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_subscribe_to_course(self):
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user.subscriptions.filter(course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        response = self.client.delete(f'/api/subscriptions/{self.course.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(self.user.subscriptions.filter(course=self.course).exists())

    def test_subscribe_unauthenticated(self):
        self.client.logout()
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 401)
