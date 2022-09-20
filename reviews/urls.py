from django.urls import path
from . import views

urlpatterns = [
    path('sport_facilities/courts/<court_id>/reviews/', views.ReviewView.as_view()),
    path('sport_facilities/courts/<court_id>/reviews/<review_id>/', views.ReviewView.as_view(), name="specific-review"),
]