from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    login_url = reverse_lazy("users_app:login")


def test_email(self):
    print("TEST EMAIL *******************************************************")
    send_mail(
        "test", "body text", "test@desarrollo.edu.py", ["angelemegeele@gmail.com"]
    )
    print("END TEST EMAIL *******************************************************")