import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    is_owner = models.BooleanField(null=True, blank=True, default=False)


    REQUIRED_FIELDS =["email", "first_name", "last_name"]
