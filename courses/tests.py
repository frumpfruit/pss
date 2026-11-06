import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from courses.models import Course

class CourseApiTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.teacher = User.objects.create_user(
            username="teacher_test", password="test-only-password",
            role="TEACHER",
        )
    def test_list_courses(self):
        response = self.client.get("/api/courses")
        self.assertEqual(response.status_code, 200)

    def test_create_course(self):
        payload = {
            "code": "TEST-API", "title": "Kelas API",
            "description": "Pengujian", "teacher_id": self.teacher.pk,
            "is_published": False,
        }
        response = self.client.post(
            "/api/courses", data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Course.objects.filter(code="TEST-API").exists())

    def test_course_not_found(self):
        response = self.client.get("/api/courses/999999")
        self.assertEqual(response.status_code, 404)
