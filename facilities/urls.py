from django.urls import path

from . import views

urlpatterns = [
    path('sport_facilities/', views.FacilityView.as_view()),
    path('sport_facilities/<sport_facility_id>/', views.FacilityDetailView.as_view(), name="sport_facility_view_update"),
    # path('sport_facilities/<sport_facility_id>/delete/', views.FacilityDeleteView.as_view(), name="sport_facility_view_delete"),
]
