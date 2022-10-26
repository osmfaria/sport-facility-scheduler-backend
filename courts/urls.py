from django.urls import path

from . import views

urlpatterns = [
    path('sport_facilities/courts/filter/<city>/<date>/', views.CourtFilterView.as_view(), name="court-filter"),
    path('sport_facilities/<facility_id>/courts/', views.CourtView.as_view(), name="court-view"),
    path('sport_facilities/courts/<court_id>/', views.CourtDetailView.as_view(), name="court_detail-view"),
    path('sport_facilities/courts/<court_id>/schedules/<date>/', views.CourtAvailableSchedulesView.as_view(), name="list_schedule-view"),
    path('sport_facilities/courts/<court_id>/non_operating_day/', views.RegisterNonOperantingDay.as_view(), name="register_non_operating_day-view"),
    path('sport_facilities/courts/<court_id>/non_operating_day/<non_operanting_day_id>/', views.DeleteNonOperantingDay.as_view(), name="delete_non_operanting_day-view"),
    path('sport_facilities/courts/<court_id>/holidays/', views.RegisterHolidayView.as_view(), name="register_holiday-view"),
    path('sport_facilities/courts/<court_id>/holidays/<holiday_id>/', views.DeleteHolidayView.as_view(), name="delete_holiday-view"),
    
]
