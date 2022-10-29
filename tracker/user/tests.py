from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from project.models import Project
from sheet.models import Sheet


class UserTestCase(TestCase):
    def setUp(self):
        # password = 'admin'
        self.user_1 = User(
            username="test_1",
            password="pbkdf2_sha256$390000$Whas2gkCnSRUZB8X70VFvn$J5XvJ3uL4kFCOivKYYFHReI0m8aQJDMkIJotoLcK7C8=",
        )
        self.user_1.save()

        self.project_1 = Project(project_name="project_1", project_owner=self.user_1)

        self.sheet_1 = Sheet(
            sheet_date=datetime.today(),
            user=self.user_1,
            project=self.project_1,
            sheet_start_time=datetime.now(),
            sheet_end_time=datetime.now() + timedelta(hours=1),
        )
        self.project_1.save()
        self.sheet_1.save()

        self.project_1.users.set([self.user_1])

        self.client = APIClient()

    def test_user_can_do_auth(self):
        response = self.client.post(
            reverse("auth"), {"username": "test_1", "password": "admin"}
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["token"], Token.objects.get(user=self.user_1.id).key)

    def test_uset_can_get_own_details(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(reverse("user-details"))

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["username"], self.user_1.username)
        self.assertEqual(data["projects"][0]["id"], self.project_1.id)
        self.assertEqual(data["sheets"][0]["id"], self.sheet_1.id)
