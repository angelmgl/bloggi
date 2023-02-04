from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from django.views.generic import View

from django.views.generic.edit import FormView

from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UpdatePasswordForm,
    VerificationForm,
)

from .models import User
from .functions import code_generator


class UserRegisterView(UserPassesTestMixin, FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users_app:login")
    redirect_field_name = reverse_lazy("core_app:home")

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        # código de registro
        code = code_generator()

        User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["full_name"],
            form.cleaned_data["custom_password"],
            gender=form.cleaned_data["gender"],
        )

        # enviar código al email del user
        subject = "Confirmar cuenta en Bloggi"
        message = f"Tu código de verificación es {code}"
        admin_email = "angel@girolabs.com"
        destination = form.cleaned_data["email"]

        send_mail(subject, message, admin_email, [destination])

        return HttpResponseRedirect(reverse("users_app:verification"))


class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("core_app:home")

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        login(self.request, user)
        return super(UserLoginView, self).form_valid(form)


class UserLogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(reverse("users_app:login"))


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/password.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("users_app:login")
    login_url = reverse_lazy("users_app:login")

    def form_valid(self, form):
        user = self.request.user
        is_auth = authenticate(
            username=user.username,
            password=form.cleaned_data["current_password"],
        )

        if is_auth:
            user.set_password(form.cleaned_data["new_password"])
            user.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class VerificationView(FormView):
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy("core_app:home")

    def form_valid(self, form):

        return super(VerificationView, self).form_valid(form)