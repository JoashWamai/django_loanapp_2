from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginuser, name='login'),
    path("register/", views.registeruser, name='register'),
    path("logout/", views.logoutUser, name='logout')
]
