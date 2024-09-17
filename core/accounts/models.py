from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import CustomUserManager


# Create your models here.


class User(AbstractUser):

    is_verified = models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return self.email
