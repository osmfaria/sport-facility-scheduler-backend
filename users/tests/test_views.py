from urllib import response
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from model_bakery import baker


from users.models import User

class UserViewTestCase(APITestCase):
    @classmethod
    def setUp(cls):
        cls.base_url = "/api/users/"
        cls.admin_data = {
            "username" : "admin",
            "password" : "12345678",
            "email" : "admin@email.com",
            "first_name" : "Admin",
            "last_name" : "Istrador"
        }
        cls.admin = User.objects.create_superuser(**cls.admin_data)
        Token.objects.create(user=cls.admin)
        cls.owner_1 = baker.make("users.User", is_owner=True)
        cls.user_1_data = {
            "username" : "userone",
            "password" : "12345678",
            "email" : "userone@email.com",
            "first_name" : "User",
            "last_name" : "One"
        }
        cls.user_1 = User.objects.create_user(**cls.user_1_data)
        Token.objects.create(user=cls.user_1)
        cls.user_2 = baker.make("users.User")

    def test_list_users(self):
        print("executando test_list_users")

        len_users_db = len(User.objects.all())
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len_users_db)

    def test_create_user(self):
        print("executando test_create_user")

        new_user = {
            "username" : "new_user",
            "password" : "12345678",
            "email" : "newuser@email.com",
            "first_name" : "New",
            "last_name" : "User"
        }

        response = self.client.post("/api/register/", new_user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], new_user["username"])
        self.assertEqual(response.data["email"], new_user["email"])
        self.assertEqual(response.data["first_name"], new_user["first_name"])
        self.assertEqual(response.data["last_name"], new_user["last_name"])
        self.assertEqual(response.data["is_owner"], False)
        self.assertNotIn("password", response.data)

    def test_create_user_missing_keys(self):
        print("executando test_create_user_missing_keys")

        new_user = {}

        response = self.client.post("/api/register/", new_user)
        self.assertEqual(response.status_code, 400)

    def test_create_owner_user(self):
        print("executando test_create_owner_user")

        new_owner = {
            "username" : "new_owner",
            "password" : "12345678",
            "email" : "newuser@email.com",
            "first_name" : "New",
            "last_name" : "User",
            "is_owner" : True
        }

        response = self.client.post("/api/register/", new_owner)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], new_owner["username"])
        self.assertEqual(response.data["email"], new_owner["email"])
        self.assertEqual(response.data["first_name"], new_owner["first_name"])
        self.assertEqual(response.data["last_name"], new_owner["last_name"])
        self.assertEqual(response.data["is_owner"], True)
        self.assertNotIn("password", response.data)

    def test_login_user(self):
        print("executando test_login_user")

        credentials = {
            "username" : self.user_1_data["username"],
            "password" : self.user_1_data["password"]
        }
        
        response = self.client.post("/api/login/", credentials)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_see_user_detail(self):
        print("executando test_see_user_detail")

        token = Token.objects.get(user__username=self.user_1.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(f"{self.base_url}{self.user_1.id}/")

        user_fields = ["id", "username", "email", "first_name", "last_name", "current_schedules", "schedule_history", "is_owner", "date_joined"]

        self.assertEqual(response.status_code, 200)

        for field in user_fields:
            self.assertIn(field, response.data)

    def test_user_details_permission(self):
        print("executando test_user_details_permission")

        token = Token.objects.get(user__username=self.user_1.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(f"{self.base_url}{self.user_2.id}/")

        self.assertEqual(response.status_code, 403)

        token_admin = Token.objects.get(user__username=self.admin.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_admin.key)

        response = self.client.get(f"{self.base_url}{self.user_2.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_own_user_last_name(self):
        print("executando test_update_own_user_last_name")

        token = Token.objects.get(user__username=self.user_1.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        updated_data= {
            "last_name" : "Last Name Updated"
        }

        response = self.client.patch(f"{self.base_url}{self.user_1.id}/",  updated_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["last_name"], updated_data["last_name"])

    def test_update_owner_permission(self):
        print("executando test_update_owner_permission")

        token = Token.objects.get(user__username=self.user_1.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        updated_data= {
            "last_name" : "Last Name Updated"
        }

        response = self.client.patch(f"{self.base_url}{self.user_2.id}/",  updated_data)
        self.assertEqual(response.status_code, 403)
        
    def test_delete_own_user(self):
        print("executando test_delete_own_user")

        token = Token.objects.get(user__username=self.user_1.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(f"{self.base_url}{self.user_1.id}/")

        self.assertEqual(response.status_code, 204)

        users_list = User.objects.all()
        self.assertNotIn(self.user_1, users_list)

    def test_delete_owner_permission(self):
        print("executando test_delete_not_own_user")

        token = Token.objects.get(user__username=self.user_1.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(f"{self.base_url}{self.user_2.id}/")
        self.assertEqual(response.status_code, 403)

        token = Token.objects.get(user__username=self.admin.username)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(f"{self.base_url}{self.user_2.id}/")
        self.assertEqual(response.status_code, 204)