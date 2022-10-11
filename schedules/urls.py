from django.urls import path

from .views import CancelScheduleView, ScheduleCreateView, SendEmail, hello

urlpatterns = [
    path('sport_facilities/courts/<court_id>/schedules/', ScheduleCreateView.as_view() , name="create_schedule-view"),
    path('sport_facilities/courts/schedules/<schedule_id>/', CancelScheduleView.as_view() , name="cancel_schedule-view"),
    path('sendemail/', SendEmail.as_view()),
    path('hello/', hello, name='hello'),
]

