from django.urls import path

from . import views

urlpatterns = [
    path('users/<user_id>/payments/', views.ListUserPaymentInformations.as_view()),
    path('users/<user_id>/payments/register/', views.PaymentInformationView.as_view()),
    path('users/<user_id>/payments/<payment_id>/', views.PaymentDetailView.as_view()),
]

