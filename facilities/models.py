import uuid
from django.db import models


class Facility(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=60, unique=True)
    email = models.EmailField(max_length=256, unique=True)
    phone_number = models.CharField(max_length=60, unique=True)

    address = models.OneToOneField("addresses.Address", on_delete=models.CASCADE, related_name="facility", null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="facilities")
