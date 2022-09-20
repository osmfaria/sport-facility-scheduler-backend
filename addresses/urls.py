from django.urls import path

from . import views

urlpatterns = [
    path('sport_facilities/<facility_id>/address/', views.AddressView.as_view(), name="sport_facility_address"),
]
