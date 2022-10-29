from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from project.models import Project

from .models import Sheet


class SheetAuthenticatedUserTestCase(TestCase):
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
        self.project_1.users.set([self.user_1, self.user_3])
        self.project_2.users.set([self.user_2])

        (
            self.sheet_user_1,
            self.sheet_user_2,
            self.sheet_user_3,
        ) = Sheet.objects.bulk_create(
            [
                Sheet(
                    sheet_date=datetime.today(),
                    user=self.user_1,
                    project=self.project_1,
                    sheet_start_time=datetime.now(),
                    sheet_end_time=datetime.now() + timedelta(hours=1),
                ),
                Sheet(
                    sheet_date=datetime.today(),
                    user=self.user_2,
                    project=self.project_2,
                    sheet_start_time=datetime.now(),
                    sheet_end_time=datetime.now() + timedelta(hours=1),
                ),
                Sheet(
                    sheet_date=datetime.today(),
                    user=self.user_3,
                    project=self.project_1,
                    sheet_start_time=datetime.now(),
                    sheet_end_time=datetime.now() + timedelta(hours=1),
                ),
            ]
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_user_can_create_own_sheet(self):
        date = datetime.today().strftime("%Y-%m-%d")
        start_time = datetime.now().strftime("%H:%M:%S")
        end_time = (datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")

        response = self.client.post(
            reverse("sheet"),
            {
                "sheet_date": date,
                "user": self.user_1.id,
                "project": self.project_1.id,
                "sheet_start_time": start_time,
                "sheet_end_time": end_time,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["user"], self.user_1.id)
        self.assertEqual(data["project"], self.project_1.id)
        sh_from_db = Sheet.objects.get(pk=data["id"])
        self.assertEqual(sh_from_db.sheet_start_time.strftime("%H:%M:%S"), start_time)

    def test_user_can_edit_own_sheet(self):
        date = datetime.today().strftime("%Y-%m-%d")
        start_time = datetime.now().strftime("%H:%M:%S")
        end_time = (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S")

        response = self.client.patch(
            reverse("sheet-details", args=[self.sheet_user_1.id]),
            {"sheet_start_time": start_time, "sheet_end_time": end_time},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        sh_from_db = Sheet.objects.get(pk=self.sheet_user_1.id)
        self.assertEqual(sh_from_db.sheet_start_time.strftime("%H:%M:%S"), start_time)
        self.assertEqual(sh_from_db.sheet_end_time.strftime("%H:%M:%S"), end_time)

    def test_user_cannot_edit_project_or_user_details(self):
        date = datetime.today().strftime("%Y-%m-%d")
        start_time = datetime.now().strftime("%H:%M:%S")
        end_time = (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S")

        response = self.client.patch(
            reverse("sheet-details", args=[self.sheet_user_1.id]),
            {"users": self.user_3.id, "project": self.project_2.id},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        sh_from_db = Sheet.objects.get(pk=self.sheet_user_1.id)
        self.assertEqual(data["user"], self.user_1.id)
        self.assertEqual(data["project"], self.project_1.id)
        self.assertEqual(sh_from_db.user_id, self.user_1.id)
        self.assertEqual(sh_from_db.project_id, self.project_1.id)

    def test_user_can_get_only_sheets_in_own_project(self):
        response = self.client.get(reverse("sheet"))

        data = response.json()

        self.assertEqual(response.status_code, 200)
        # only users, who belongs to project self.project_1 should be shown
        self.assertEqual(
            [i["user"] for i in data],
            [user.id for user in Project.objects.get(pk=self.project_1.id).users.all()],
        )

    def test_user_cannot_edit_sheet_user_same_project(self):
        response = self.client.patch(
            reverse("sheet-details", args=[self.sheet_user_3.id]),
            {},
        )
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, "Sheets can be modified only by sheet owner.")

    def test_user_cannot_edit_sheet_other_project_user(self):
        response = self.client.patch(
            reverse("sheet-details", args=[self.sheet_user_2.id]),
            {},
        )
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, "Sheets can be modified only by sheet owner.")

    def test_user_cannot_create_sheet_wrong_time(self):
        date = datetime.today().strftime("%Y-%m-%d")
        start_time = datetime.now().strftime("%H:%M:%S")
        end_time = (datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S")

        response = self.client.post(
            reverse("sheet"),
            {
                "sheet_date": date,
                "user": self.user_1.id,
                "project": self.project_1.id,
                "sheet_start_time": start_time,
                "sheet_end_time": end_time,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data["non_field_errors"][0], "End time must be greater than start time"
        )

    def test_user_cannot_update_sheet_wrong_time(self):
        date = datetime.today().strftime("%Y-%m-%d")
        start_time = datetime.now().strftime("%H:%M:%S")
        end_time = (datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S")

        response = self.client.patch(
            reverse("sheet-details", args=[self.sheet_user_1.id]),
            {
                "sheet_date": date,
                "user": self.user_1.id,
                "project": self.project_1.id,
                "sheet_start_time": start_time,
                "sheet_end_time": end_time,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data["non_field_errors"][0], "End time must be greater than start time"
        )
