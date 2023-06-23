import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


class DayOfTheWeek(models.TextChoices):
    MONDAY = "MONDAY",
    TUESDAY = "TUESDAY",
    WEDNESDAY = "WEDNESDAY",
    THURSDAY = "THURSDAY",
    FRIDAY = "FRIDAY",
    SATURDAY = "SATURDAY",
    SUNDAY = "SUNDAY",


class NonOperatingDay(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    court = models.OneToOneField("courts.Court", on_delete=models.CASCADE, related_name="non_operating_days")
    regular_day_off = ArrayField(models.CharField(max_length=9, choices=DayOfTheWeek.choices, default=list))



class Holiday(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    court = models.ForeignKey("courts.Court", on_delete=models.CASCADE, related_name="holidays")
    holiday = models.DateField()

    
class Court(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=127)
    capacity = models.PositiveIntegerField()
    is_indoor = models.BooleanField(default=False)
    price_by_hour = models.DecimalField(max_digits=10, decimal_places=2)
    max_schedule_range_in_days = models.PositiveIntegerField()
    sport = models.CharField(max_length=127)

    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    
    sport_facility = models.ForeignKey("facilities.Facility", on_delete=models.CASCADE, related_name="courts")
