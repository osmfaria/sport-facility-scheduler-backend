from uuid import UUID

from addresses.models import Address
from django.test import TestCase


class AddressTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.address_data = {
            "street": "Rodovia Aroldo 111",
            "number": "123",
            "zipcode": "12334",
            "state": "SP"
        }

        cls.address = Address.objects.create(**cls.address_data)

    def test_address_attributes(self):
        print("test address_attributes")

        self.assertEqual(type(self.address.id), UUID)

        address_instance_object = vars(self.address)

        for key, data in self.address_data.items():
            self.assertEqual(address_instance_object[key], data)

    def test_address_size_limits(self):
        print("test address_size_limits")

        address_instance_object = vars(self.address)

        expected_less_len_1 = 20
        expected_less_len_2 = 10
        expected_less_len_3 = 60

        self.assertLess(len(address_instance_object["street"]), expected_less_len_3)
        self.assertLess(len(address_instance_object["number"]), expected_less_len_2)
        self.assertLess(len(address_instance_object["state"]), expected_less_len_1)
