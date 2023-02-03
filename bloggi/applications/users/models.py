from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """clase para generar mi modelo personalizado de usuarios"""

    class GenderChoices(models.TextChoices):
        MAN = "1", "hombre"
        WOMAN = "2", "mujer"

    username = models.CharField("nombre de usuario", max_length=50, unique=True)
    full_name = models.CharField("nombre completo", max_length=150)
    gender = models.CharField(
        "género", max_length=1, choices=GenderChoices.choices, blank=True, null=True
    )
    email = models.EmailField("correo electrónico", max_length=254, unique=True)
    is_staff = models.BooleanField("staff", default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"

    # para que la terminal nos pida estos datos al crear un superuser
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = UserManager()
