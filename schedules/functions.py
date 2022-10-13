from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


def create_add_to_calendar(date, duration, address, court):

    initial_date = date.strftime("%Y%m%dT%H0000")
    final_date = (date + timedelta(hours=duration)).strftime("%Y%m%dT%H0000")

    court_name = court.name.replace(" ", "+")
    sport_facility = court.sport_facility.name.replace(" ", "+")
    street = address.street.replace(" ", "+")
    city = address.city.replace(" ", "+")
    zipcode = address.zipcode.replace(" ", "+")

    return f"https://calendar.google.com/calendar/u/0/r/eventedit?text=Court+Reservation&dates={initial_date}/{final_date}&details=Court:+{court_name}%0ASport+Facility:+{sport_facility}%0ADuration:+{duration}&location={address.number}+{street},+{city},+{address.state}+{zipcode}"


def sendmail(subject, recipient, sender, court, duration, date_time, user):

    address_path = court.sport_facility.address
    add_to_calendar_link = create_add_to_calendar(date_time, duration, address_path, court)
    address = f"{address_path.number} {address_path.street.capitalize()}, {address_path.state.upper()}, {address_path.city.capitalize()}, {address_path.zipcode.upper()}"
    date_time_formated = date_time.strftime("%a, %b %d, %-I:00 %p")
    
    ctx = {"court": court, "duration": duration, "date_time": date_time_formated, "user": user, "address": address, "calendar": add_to_calendar_link}
    message = render_to_string("schedule.html", ctx)
    text_content = strip_tags(message)

    email = mail.EmailMultiAlternatives(subject, text_content, sender, recipient)
    email.attach_alternative(message, "text/html")
    email.send()