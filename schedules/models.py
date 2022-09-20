import uuid

from django.db import models


class Schedule(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    datetime = models.DateTimeField()
    number_of_hours = models.IntegerField()
    
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="schedules")
    court = models.ForeignKey("courts.Court", on_delete=models.CASCADE, related_name="schedules")
