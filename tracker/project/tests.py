from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Project


class ProjectAuthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.user_1, self.user_2, self.user_3 = User.objects.bulk_create(
            [User(username="test_1"), User(username="test_2"), User(username="test_3")]
        )
        self.project_1, self.project_2 = Project.objects.bulk_create(
            [
                Project(project_name="project_1", project_owner=self.user_1),
                Project(project_name="project_2", project_owner=self.user_2),
            ]
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_user_can_create_project(self):
        response = self.client.post(
            reverse("project"),
            {"project_name": "created_project_1", "project_owner": self.user_1.id},
        )

        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["project_owner"], self.user_1.id)
        pr_from_db = Project.objects.get(pk=data['id'])
        self.assertEqual(pr_from_db.project_name, "created_project_1")

    def test_user_can_edit_own_project(self):
        response = self.client.patch(
            reverse("project-details", args=[self.project_1.id]),
            {"project_name": "edited_project", "project_owner": self.user_2.id},
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["project_owner"], self.user_2.id)
        self.assertEqual(data["project_name"], "edited_project")
        pr_from_db = Project.objects.get(pk=data['id'])
        self.assertEqual(pr_from_db.project_name, "edited_project")

    def test_user_cannot_edit_not_own_project(self):
        response = self.client.patch(
            reverse("project-details", args=[self.project_2.id]),
            {"project_name": "edited_project", "project_owner": self.user_1.id},
        )

        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, "Only project owners are allowed to perform changes.")
        pr_from_db = Project.objects.get(pk=self.project_2.id)
        self.assertEqual(pr_from_db.project_name, "project_2")

    def test_user_cannot_delete_not_own_project(self):
        response = self.client.delete(
            reverse("project-details", args=[self.project_2.id])
        )

        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, "Only project owners are allowed to perform changes.")
        pr_from_db = Project.objects.get(pk=self.project_2.id)
        self.assertEqual(pr_from_db.project_name, "project_2")

    def test_users_can_be_assigned_to_project(self):
        response = self.client.patch(
            reverse("project-details", args=[self.project_1.id]),
            {"users": [self.user_1.id, self.user_3.id]},
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["users"], [self.user_1.id, self.user_3.id])
        pr_from_db = Project.objects.get(pk=self.project_1.id)
        self.assertEqual(
            [user.id for user in pr_from_db.users.all()],
            [self.user_1.id, self.user_3.id],
        )


class ProjectNotAuthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.user_1, self.user_2, self.user_3 = User.objects.bulk_create(
            [User(username="test_1"), User(username="test_2"), User(username="test_3")]
        )
        self.project_1, self.project_2 = Project.objects.bulk_create(
            [
                Project(project_name="project_1", project_owner=self.user_1),
                Project(project_name="project_2", project_owner=self.user_2),
            ]
        )

        self.client = APIClient()

    def test_unauthorized_user_cannot_create_project(self):
        response = self.client.post(
            reverse("project"),
            {"project_name": "project_1", "project_owner": self.user_1.id},
        )

        self.assertEqual(response.status_code, 401)

    def test_unauthorized_user_cannot_edit_project(self):
        response = self.client.patch(
            reverse("project"),
            {"project_name": "project_1", "project_owner": self.user_1.id},
        )

        self.assertEqual(response.status_code, 401)
