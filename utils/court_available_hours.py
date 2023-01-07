from courts.models import NonOperatingDay, Holiday
from schedules.models import Schedule
from datetime import datetime, timedelta


def get_week_day(day):
    days_of_the_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    return days_of_the_week[day]


def check_is_date_in_the_past(input_date, obj, today):
    return (input_date.date() < today.date())
        

def check_date_in_an_available_period(input_date, obj, today):
    days = vars(obj)['max_schedule_range_in_days']

    return (input_date.date() > today.date() + timedelta(days=days))


def check_court_is_open(input_date, obj, today):
    court_id = vars(obj)['id']
    
    weekday = input_date.weekday()
    
    non_operating_day = NonOperatingDay.objects.filter(court=court_id, regular_day_off=get_week_day(weekday))
    holiday = Holiday.objects.filter(court_id=court_id, holiday=input_date)
    
    is_after_hours = (input_date.date() == today.date()) and (today.hour > obj.closing_hour.hour)
    
    if non_operating_day  or holiday or is_after_hours:
        return False

    return True


def get_starting_hour(input_date, obj, today):
    if input_date.date() == today.date():
        return today.hour + 1

    return obj.opening_hour.hour
    

def get_booked_hours(input_date, obj):
     schedules_booked = Schedule.objects.filter(court=obj, datetime__date=input_date)

     return [schedule.datetime.hour for schedule in schedules_booked]


def list_court_available_hours(input_date, obj):
    today = datetime.now()

    starting_hour = get_starting_hour(input_date, obj, today)
    
    booked_hours = get_booked_hours(input_date, obj)

    if check_is_date_in_the_past(input_date, obj, today):
        return {"detail": "You can't schedule in the past... yet"}

    if check_is_date_in_the_past(input_date, obj, today):
        return {"detail": "You can't schedule in the past... yet"}

    if not check_court_is_open(input_date, obj, today):
        return {"detail": "court is closed"}
    
    return [hour for hour in range(starting_hour, obj.closing_hour.hour) if hour not in booked_hours]
