from django.contrib.auth.models import AbstractUser
from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('USER', 'User'),
#         ('ADMIN', 'Admin'),
#     )

#     role = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='USER'
#     )

#     pan_number = models.CharField(
#         max_length=10,
#         unique=True,
#         null=True,
#         blank=True
#     )

#     phone = models.CharField(   # ✅ ADD THIS
#         max_length=15,
#         null=True,
#         blank=True
#     )
class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='USER'
    )

    full_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    pan_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )

    aadhaar_number = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    
    dob = models.DateField(   # ✅ Add this
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)