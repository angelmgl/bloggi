from django.urls import path
from . import views

app_name = "core_app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("test/", views.test_email),
]