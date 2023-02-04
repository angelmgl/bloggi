from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):

    custom_password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Crea una contraseña"}),
    )

    repeat_password = forms.CharField(
        label="Confirma tu contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repite tu contraseña"}),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "gender",
            "email",
        )

    def clean_repeat_password(self):
        if self.cleaned_data["custom_password"] != self.cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Las contraseñas no coinciden")

        if len(self.cleaned_data["custom_password"]) <= 5:
            self.add_error("custom_password", "La contraseña es muy corta")


class UserLoginForm(forms.Form):

    username = forms.CharField(
        label="Nombre de usuario",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingresa tu usuario",
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Ingresa tu contraseña"}),
    )

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if not authenticate(username=username, password=password):
            raise forms.ValidationError(
                "Datos incorrectos, verifica e intenta nuevamente"
            )

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    current_password = forms.CharField(
        label="Contraseña actual",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Ingresa tu contraseña actual"}
        ),
    )

    new_password = forms.CharField(
        label="Contraseña nueva",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Crea una contraseña nueva"}),
    )

    repeat_password = forms.CharField(
        label="Confirma tu contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repite tu contraseña"}),
    )

    def clean_repeat_password(self):
        if self.cleaned_data["new_password"] != self.cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Las contraseñas no coinciden")

        if len(self.cleaned_data["new_password"]) <= 5:
            self.add_error("new_password", "La contraseña es muy corta")


class VerificationForm(forms.Form):

    code = forms.CharField(
        label="Introduzca el código enviado a su correo",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Introduzca su código de verificación"}
        ),
    )
