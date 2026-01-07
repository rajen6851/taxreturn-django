from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)  # optional now
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    pan_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # username not required

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]  # auto-generate username
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
