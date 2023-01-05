from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username