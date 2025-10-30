from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import CustomManager

# Create your models here.

class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManager()

    def __str__(self):
        return self.email