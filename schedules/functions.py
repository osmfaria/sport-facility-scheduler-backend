from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from project import settings


def create_add_to_calendar(date, duration, address, court):

    initial_date = date.strftime("%Y%m%dT%H0000")
    final_date = (date + timedelta(hours=duration)).strftime("%Y%m%dT%H0000")

    court_name = court.name.replace(" ", "+")
    sport_facility = court.sport_facility.name.replace(" ", "+")
    street = address.address1.replace(" ", "+")
    city = address.city.replace(" ", "+")
    zipcode = address.zipcode.replace(" ", "+")

    return f"https://calendar.google.com/calendar/u/0/r/eventedit?text=Court+Reservation&dates={initial_date}/{final_date}&details=Court:+{court_name}%0ASport+Facility:+{sport_facility}%0ADuration:+{duration}&location={street},+{city},+{address.state}+{zipcode}"


def sendmail(subject, recipient, court, duration, date_time, user, template):

    address_path = court.sport_facility.address
    add_to_calendar_link = create_add_to_calendar(date_time, duration, address_path, court)
    address = f"{address_path.address1.capitalize()},  {address_path.address2 + ', ' if address_path.address2 else ''}{address_path.state.upper()}, {address_path.city.capitalize()}, {address_path.zipcode.upper()}"
    date_time_formated = date_time.strftime("%a, %b %d, %-I:00 %p")
    
    ctx = {"court": court, "duration": duration, "date_time": date_time_formated, "user": user, "address": address, "calendar": add_to_calendar_link}
    message = render_to_string(template, ctx)
    text_content = strip_tags(message)

    email = mail.EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, recipient)
    email.attach_alternative(message, "text/html")
    email.send()