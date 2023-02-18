from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("password/", views.UpdatePasswordView.as_view(), name="password"),
    path("activate/<str:key>/", views.ActivateView.as_view(), name="activate"),
    path("wait/", views.WaitActivationView.as_view(), name="wait"),
]
