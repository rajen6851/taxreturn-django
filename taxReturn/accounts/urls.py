# accounts/urls.py
from django.urls import path
from .views import signup_view, login_view, logout_view
from . import views

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('my-account/', views.personal_details, name='personal_details'),

]
