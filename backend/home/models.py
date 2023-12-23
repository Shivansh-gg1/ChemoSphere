from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import UserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=50, default=" ")
    email = models.EmailField(unique=True)
    is_logged = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.id} | {self.email} | {self.first_name} {self.last_name}"