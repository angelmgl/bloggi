from django.contrib import admin
from .models import User, ActivationKey

# Register your models here.
admin.site.register([User, ActivationKey])

