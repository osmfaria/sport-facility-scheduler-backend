from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.ListUsersView.as_view()),
    path('register/', views.RegisterUserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('users/<user_id>/', views.UserDetailsView.as_view()),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
