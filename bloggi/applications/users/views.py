from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import redirect, get_object_or_404

from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UpdatePasswordForm,
)

from .models import User, ActivationKey
from .functions import generate_activation_key, send_activation_email


class UserRegisterView(UserPassesTestMixin, FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users_app:login")
    redirect_field_name = reverse_lazy("core_app:home")

    def test_func(self):
        """
        esta función ayuda a restringir el acceso a la vista de registro a los
        usuarios que no han iniciado sesión, ya que la vista solo debería estar
        disponible para los usuarios que aún no tienen una cuenta en la aplicación.
        """
        return self.request.user.is_anonymous

    def form_valid(self, form):
        user = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["full_name"],
            form.cleaned_data["custom_password"],
            gender=form.cleaned_data["gender"],
        )

        activation_key = generate_activation_key(user)
        activation_url = self.request.build_absolute_uri(
            reverse("users_app:activate", args=[activation_key])
        )
        send_activation_email(user, activation_url)

        return HttpResponseRedirect(reverse("users_app:wait"))


class WaitActivationView(TemplateView):
    template_name = "users/wait.html"


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


class ActivateView(View):
    def get(self, request, key):
        # Get the activation key
        activation_key = get_object_or_404(ActivationKey, key=key)

        # Activate the user account
        user = activation_key.user
        user.is_active = True
        user.save()

        # Log in the user
        # user = authenticate(username=user.username, password=user.password)
        # login(request, user)

        # Delete the activation key
        activation_key.delete()

        # Redirect to a success page
        return redirect("core_app:home")
