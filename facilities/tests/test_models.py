from uuid import UUID

from addresses.models import Address
from django.test import TestCase
from facilities.models import Facility
from users.models import User


class FacilityTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username": "mariah",
            "password": "1234",
            "email": "maria@hotmail.com",
            "first_name": "mariah",
            "last_name": "serodioh",
            "is_owner": True
        }
        cls.user_data_2 = {
            "username": "afonso",
            "password": "1234",
            "email": "afonso@hotmail.com",
            "first_name": "afonso",
            "last_name": "barbosa",
            "is_owner": True
        }

        cls.sport_facility_data = {
            "name": "mariah sport",
            "email": "mariag@hotmail.com",
            "phone_number": "13456-2121",
        }

        cls.user_instance = User.objects.create(**cls.user_data)

        cls.user_instance_2 = User.objects.create(**cls.user_data_2)

        cls.sport_facility_instance = Facility.objects.create(**cls.sport_facility_data, user=cls.user_instance)

        cls.address = Address.objects.create(street="Rodovia Aroldo, 111", number="2121", zipcode="2345",state="SP")

        cls.address_2 = Address.objects.create(street="Av Aroldo, 22", number="2", zipcode="2111",state="SP")

    def test_sport_facility_attributes(self):
        print("test sport_facility_attributes")

        self.assertEqual(type(self.sport_facility_instance.id), UUID)

        sport_facility_instance_object = vars(self.sport_facility_instance)

        for key, data in self.sport_facility_data.items():
            self.assertEqual(sport_facility_instance_object[key], data)

    def test_sport_facility_user_foreignkey(self):
        print("test sport_facility_user_foreignkey")
        sport_facility_user_id = Facility.objects.filter(id=self.sport_facility_instance.id).values_list("user", flat=True)

        self.assertEqual(sport_facility_user_id[0], self.user_instance.id)

        sport_facility_user_id = self.user_instance_2

        sport_facility_user_id.save()

        self.assertNotEqual(sport_facility_user_id.id, self.user_instance.id)

    def test_sport_facility_addres_one_to_one(self):
        print("test sport_facility_addres_one_to_one")

        self.sport_facility_instance.address = self.address

        self.assertEqual(self.sport_facility_instance.address, self.address)

        self.sport_facility_instance.save()

        self.sport_facility_instance.address = self.address_2

        self.assertNotEqual(self.sport_facility_instance.address, self.address)
