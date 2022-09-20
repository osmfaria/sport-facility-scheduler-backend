from courts.models import Court, NonOperatingDay, Holiday
from datetime import datetime, timedelta
from schedules.models import Schedule
import ipdb

def get_week_day(day):
    days_of_the_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    return days_of_the_week[day]

def list_court_available_hours(input_date, obj):
    today = datetime.now()
    # ipdb.set_trace()

    if input_date.date() < today.date():
        return {"detail": "You can't schedule in the past... yet"}
    
    days = vars(obj)['max_schedule_range_in_days']

    if input_date.date() > today.date() + timedelta(days=days):
        return {"detail": "You can't schedule that long in the future."} 

    court_id = vars(obj)['id']
    
    weekday = input_date.weekday()
    
    non_operating_day = NonOperatingDay.objects.filter(court=court_id, regular_day_off=get_week_day(weekday))
    holiday = Holiday.objects.filter(court_id=court_id, holiday=input_date)
    
    is_after_hours = (input_date.date() == today.date()) and (today.hour > obj.closing_hour.hour)
    
    if non_operating_day  or holiday or is_after_hours:
        return {"detail": "court is closed"}
    
    starting_hour = obj.opening_hour.hour
    
    if input_date.date() == today.date():
        starting_hour = today.hour + 1
    
    schedules_booked = Schedule.objects.filter(court=obj, datetime__date=input_date)

    booked_hours = [schedule.datetime.hour for schedule in schedules_booked]
    
    return [hour for hour in range(starting_hour, obj.closing_hour.hour) if hour not in booked_hours]