from django.urls import reverse
from facilities.models import Facility
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User


class FacilityViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = baker.make("users.User", is_owner=True)

        cls.user_2 = baker.make("users.User", is_owner=True)

        cls.user_not_owner = baker.make("users.User")

        cls.admin_data = {
            "username" : "admin",
            "password" : "12345678",
            "email" : "admin@email.com",
            "first_name" : "Admin",
            "last_name" : "Istrador"
        }
        cls.admin = User.objects.create_superuser(**cls.admin_data)

        Token.objects.create(user=cls.admin)

        cls.sport_facility = baker.make("facilities.Facility", user=cls.user)

        cls.sport_facility_2 = baker.make("facilities.Facility", user=cls.user)

        cls.sport_facility_3 = baker.make("facilities.Facility", user=cls.user)

        Token.objects.create(user=cls.user)

        Token.objects.create(user=cls.user_2)

        Token.objects.create(user=cls.user_not_owner)

        cls.base_url = "/api/sport_facilities/"

    def test_list_facility_view(self):
        print("test list_facility_view")
        token = Token.objects.get(user__id=self.user.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.get(self.base_url)

        all_sport_facilities = Facility.objects.all()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), len(all_sport_facilities))

    def test_create_facility_view(self):
        print("test create_facility_view")

        token = Token.objects.get(user__id=self.user.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        sport_facility_data = {
            "name": "andre",
            "email": "andre@hotmail.com",
            "phone_number": "123456-7223",
            "user": self.user,
        }

        response = self.client.post(self.base_url, sport_facility_data)

        self.assertEqual(response.status_code, 201)
        expected_keys = ["id", "name", "email", "phone_number", "user", "address_id"]

        for key in expected_keys:
            self.assertIn(key, response.data)

        for key in response.data.keys():
            self.assertIn(key, expected_keys)

    def test_facility_views_permissions(self):
        print("test facility_views_permissions")

        token_owner = Token.objects.get(user__id=self.user.id)
        token_admin = Token.objects.get(user__id=self.admin.id)
        token_not_owner = Token.objects.get(user__id=self.user_not_owner.id)

        sport_facility_data = {
            "name": "andre",
            "email": "andre@hotmail.com",
            "phone_number": "123456-7223",
            "user": self.user,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_owner.key)

        response = self.client.post(self.base_url, sport_facility_data)

        self.assertEqual(response.status_code, 201)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_admin.key)

        response = self.client.post(self.base_url, sport_facility_data)

        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_not_owner.key)

        response = self.client.post(self.base_url, sport_facility_data)

        self.assertEqual(response.status_code, 403)

    def test_update_facility_detail_view(self):
        print("test update_facility_detail_view")

        sport_facility_update = {"name": "andre sport update"}

        token = Token.objects.get(user__id=self.user.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)


        response = self.client.patch(reverse("sport_facility_view_update", kwargs={"sport_facility_id": self.sport_facility.id}), sport_facility_update)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["name"], sport_facility_update["name"])

    def test_update_facility_permissions(self):
        print("test update_facility_permissions")

        sport_facility_update = {"name": "andre sport update"}

        admin_token = Token.objects.get(user__id=self.admin.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + admin_token.key)

        response = self.client.patch(reverse("sport_facility_view_update", kwargs={"sport_facility_id": self.sport_facility.id}), sport_facility_update)

        self.assertEqual(response.status_code, 403)

    def test_delete_facility_view(self):
        print("test delete_facility_view")

        all_sport_facility = Facility.objects.all()

        token = Token.objects.get(user__id=self.user.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.delete(reverse("sport_facility_view_delete", kwargs={"sport_facility_id": self.sport_facility.id}))

        self.assertEqual(response.status_code, 204)

        self.assertNotIn(self.sport_facility, all_sport_facility)

    def test_delete_facility_permissions(self):
        print("test delete_facility_permissions")

        not_owner_token = Token.objects.get(user__id=self.user_2.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + not_owner_token.key)

        response = self.client.delete(reverse("sport_facility_view_delete", kwargs={"sport_facility_id": self.sport_facility_2.id}))

        self.assertEqual(response.status_code, 403)

        admin_token = Token.objects.get(user__id=self.admin.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + admin_token.key)

        response = self.client.delete(reverse("sport_facility_view_delete", kwargs={"sport_facility_id": self.sport_facility_2.id}))

        self.assertEqual(response.status_code, 204)

        owner_token = Token.objects.get(user__id=self.user.id)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + owner_token.key)

        response = self.client.delete(reverse("sport_facility_view_delete", kwargs={"sport_facility_id": self.sport_facility_3.id}))

        self.assertEqual(response.status_code, 204)
