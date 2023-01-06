from django.urls import path

from .views import CancelScheduleView, ScheduleCreateView, ScheduleFilterView

urlpatterns = [
    path('sport_facilities/courts/<court_id>/schedules/', ScheduleCreateView.as_view() , name="create_schedule-view"),
    path('sport_facilities/courts/<court_id>/management/<initial_date>/<final_date>/', ScheduleFilterView.as_view() , name="list_schedule-view"),
    path('sport_facilities/courts/schedules/<schedule_id>/', CancelScheduleView.as_view() , name="cancel_schedule-view"),
]

