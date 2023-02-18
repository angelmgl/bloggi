from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """clase para generar mi modelo personalizado de usuarios"""

    class GenderChoices(models.TextChoices):
        MAN = "1", "Hombre"
        WOMAN = "2", "Mujer"

    username = models.CharField("nombre de usuario", max_length=50, unique=True)
    email = models.EmailField("correo electrónico", max_length=254, unique=True)
    full_name = models.CharField("nombre completo", max_length=150)
    gender = models.CharField(
        "género", max_length=1, choices=GenderChoices.choices, blank=True, null=True
    )
    is_staff = models.BooleanField("staff", default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    # para que la terminal nos pida estos datos al crear un superuser
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = UserManager()


class ActivationKey(models.Model):
    """ clase para generar una clave de activación """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.user.full_name}"