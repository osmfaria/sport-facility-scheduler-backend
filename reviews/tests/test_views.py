from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework.views import status
from users.models import User
from facilities.models import Facility
from courts.models import Court
from django.urls import reverse

class ReviewViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username" : "user",
            "password" : "1234",
            "email" : "user@email.com",
            "first_name" : "User",
            "last_name" : "Test",
            "is_owner": True
        }

        cls.user2_data = {
            "username" : "user2",
            "password" : "1234",
            "email" : "user2@email.com",
            "first_name" : "User2",
            "last_name" : "Test",
            "is_owner": True
        }

        cls.user_1 = User.objects.create_user(**cls.user_data)
        cls.user_2 = User.objects.create_user(**cls.user2_data)

        cls.court = baker.make('courts.Court')

        cls.facility = baker.make('facilities.Facility', user=cls.user_1)

        cls.review_data = {
            "rating": 2,
            "review": "Lorem Ipsum"
        }

        cls.review_data_2 = {
            "rating": 3,
            "review": "Lorem Ipsum 2"
        }

    def test_can_create_review(self):
        login_response = self.client.post("/api/login/", data={"username": self.user_data['username'], "password": self.user_data['password']})
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data)

        expected_status_code = status.HTTP_201_CREATED

        self.assertEqual(expected_status_code, response.status_code)
    
    def test_cant_create_two_review_in_same_court(self):
        login_response = self.client.post("/api/login/", data={"username": self.user_data['username'], "password": self.user_data['password']})
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response1 = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data)
        response2 = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data_2)

        expected_status_code1 = status.HTTP_201_CREATED
        expected_status_code2 = status.HTTP_400_BAD_REQUEST

        self.assertEqual(expected_status_code1, response1.status_code)   
        self.assertEqual(expected_status_code2, response2.status_code)

    def test_review_fields(self):
        login_response = self.client.post("/api/login/", data={"username": self.user_data['username'], "password": self.user_data['password']})
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data)

        expected_return_fields = ('id', 'user', 'court', 'rating', 'review')

        self.assertEqual(len(response.data.keys()), 5)

        return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, return_fields)

    def test_patch_review(self):
        login_response = self.client.post("/api/login/", data={"username": self.user_data['username'], "password": self.user_data['password']})
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        post_response = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data)

        review_id = post_response.data['id']

        patch_response = self.client.patch(reverse("specific-review", kwargs={"court_id": self.court.id, "review_id": review_id}), data={"street": "patch"})

        expected_status_code = status.HTTP_200_OK

        self.assertEqual(expected_status_code, patch_response.status_code) 

    def test_patch_with_non_owner(self):
        login1_response = self.client.post("/api/login/", data={"username": self.user_data['username'], "password": self.user_data['password']})
        token1 = login1_response.data['token']

        login2_response = self.client.post("/api/login/", data={"username": self.user2_data['username'], "password": self.user2_data['password']})
        token2 = login2_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token1)

        post_response = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data)

        review_id = post_response.data['id']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token2)

        patch_response = self.client.patch(reverse("specific-review", kwargs={"court_id": self.court.id, "review_id": review_id}), data={"street": "patch"})

        expected_status_code = status.HTTP_403_FORBIDDEN

        self.assertEqual(expected_status_code, patch_response.status_code)

    def test_review_delete(self):
        login1_response = self.client.post("/api/login/", data={"username": self.user_data['username'], "password": self.user_data['password']})
        token1 = login1_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token1)

        post_response = self.client.post(f'/api/sport_facilities/courts/{self.court.id}/reviews/', data=self.review_data)

        review_id = post_response.data['id']

        patch_response = self.client.delete(reverse("specific-review", kwargs={"court_id": self.court.id, "review_id": review_id}))

        expected_status_code = status.HTTP_204_NO_CONTENT

        self.assertEqual(expected_status_code, patch_response.status_code)
  



