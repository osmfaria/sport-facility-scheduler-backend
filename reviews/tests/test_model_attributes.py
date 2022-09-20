from django.db.utils import IntegrityError
from django.test import TestCase
from model_bakery import baker

from reviews.models import Review

class ReviewTestModelAttributes(TestCase):
    @classmethod
    def setUp(cls):
        cls.review_data = {
            "rating": 2,
            "review": "Lorem Ipsum"
        }

        cls.review = baker.make(
            "reviews.Review",
            rating=cls.review_data['rating'],
            review=cls.review_data['review']
        )

    def test_review_fields(self):
        self.assertEqual(
            self.review.rating, self.review_data["rating"]
        )
        self.assertEqual(self.review.review, self.review_data["review"])
   
    def test_review_max_length(self):
        expected_max_length = 250
        result_max_length = self.review._meta.get_field("review").max_length

        self.assertEqual(result_max_length, expected_max_length)

    def test_rating_validators(self):
        self.review._meta.get_field("rating")._validators[0].limit_value = 10
        self.review._meta.get_field("rating")._validators[1].limit_value = 1





    