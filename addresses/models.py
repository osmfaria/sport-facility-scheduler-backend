import uuid

from django.db import models


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    address1 = models.CharField(max_length=127)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=30, default="Canada")
    map_image = models.CharField(max_length=250)
