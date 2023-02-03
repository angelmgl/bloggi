from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    def _create_user(
        self,
        username,
        email,
        full_name,
        password,
        is_staff,
        is_superuser,
        **extra_fields
    ):
        user = self.model(
            username=username,
            email=email,
            full_name=full_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, full_name, password=None, **extra_fields):
        self._create_user(
            username, email, full_name, password, False, False, **extra_fields
        )

    def create_superuser(
        self, username, email, full_name, password=None, **extra_fields
    ):
        return self._create_user(
            username, email, full_name, password, True, True, **extra_fields
        )
