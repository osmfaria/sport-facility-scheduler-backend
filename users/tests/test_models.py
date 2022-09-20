
from django.test import TestCase
from model_bakery import baker
from django.db.utils import IntegrityError
import uuid

from users.models import User

class UserModelTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.user_1 = baker.make(
            "users.User",
            username="userOne",
            email="user_one@email.com"
        )

    def test_user_fields(self):
        self.assertIsInstance(self.user_1.id, uuid.UUID)
        self.assertIsInstance(self.user_1.username, str)
        self.assertIsInstance(self.user_1.email, str)
        self.assertIsInstance(self.user_1.first_name, str)
        self.assertIsInstance(self.user_1.username, str)
        self.assertIsInstance(self.user_1.last_name, str)
        self.assertIsInstance(self.user_1.is_owner, bool)
        self.assertIsInstance(self.user_1.is_superuser, bool)

    def test_fields_max_length(self):
        print("executando test_fields_max_length")

        user = User.objects.get(username="userOne")
        username_max_length = user._meta.get_field("username").max_length
        email_max_length = user._meta.get_field("email").max_length
        first_name_max_length = user._meta.get_field("first_name").max_length
        last_name_max_length = user._meta.get_field("last_name").max_length

        self.assertEqual(username_max_length, 60)
        self.assertEqual(email_max_length, 60)
        self.assertEqual(first_name_max_length, 60)
        self.assertEqual(last_name_max_length, 60)

    def test_username_uniqueness(self):
        print("executando test_username_uniqueness")

        user = {
            "username" : self.user_1.username,
            "password" : "12345678",
            "email" : "random@email.com",
            "first_name": "Username",
            "last_name": "Already Registerd"
        }

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**user)


    def test_email_uniqueness(self):
        print("executando test_email_uniqueness")

        user = {
            "username" : "Random Name",
            "password" : "12345678",
            "email" : self.user_1.email,
            "first_name": "Email",
            "last_name": "Already Registerd"
        }

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**user)
            
    def test_is_owner_default_value(self):
        print("executando test_is_owner_default_value")

        self.assertEqual(self.user_1.is_owner, False)

    # def test_is_id_uuid(self):
    #     print("executando test_is_id_uuid")

    #     self.assertTrue(isinstance(self.user_1.id, uuid.UUID))