from schedules.models import Schedule

def validate_unique_together(datetime, obj):
    schedule_already_exists = Schedule.objects.filter(datetime=datetime, court=obj)
    if schedule_already_exists:
        True

    return False