from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    login_url = reverse_lazy("users_app:login")


def test_email(self):
    print("TEST EMAIL *******************************************************")
    send_mail(
        "test", "body text", settings.EMAIL_HOST_USER, ["angelemegeele@gmail.com"]
    )
    print("END TEST EMAIL *******************************************************")
    return HttpResponse('Correo enviado')