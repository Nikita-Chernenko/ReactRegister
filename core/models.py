from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    STUFF_CHOICES = (
        ('T', 'Teacher'),
        ('S', 'Student'),
        ('A', 'Admin')
    )
    staff = models.CharField(max_length=1, choices=STUFF_CHOICES)
