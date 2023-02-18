# helpers de la app users
import hashlib
import random
from django.utils import timezone
from .models import ActivationKey
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def generate_activation_key(user):
    salt = hashlib.sha1(str(random.random()).encode("utf-8")).hexdigest()[:5]
    activation_key = hashlib.sha1((salt + user.email).encode("utf-8")).hexdigest()
    activation_key_obj = ActivationKey(
        user=user, key=activation_key, created_date=timezone.now()
    )
    activation_key_obj.save()
    return activation_key_obj.key


def send_activation_email(user, activation_url):
    subject = "Activa tu cuenta en Bloggi"
    message = render_to_string(
        "emails/activation.html", {"full_name": user.full_name, "activation_url": activation_url}
    )

    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
    mail.content_subtype = "html"
    mail.send()
