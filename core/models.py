from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from DjangoReact import settings


class User(AbstractUser):
    STUFF_CHOICES = (
        ('T', 'Teacher'),
        ('S', 'Student'),
        ('A', 'Admin')
    )
    staff = models.CharField(max_length=1, choices=STUFF_CHOICES)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)