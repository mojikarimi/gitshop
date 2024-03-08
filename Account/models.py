from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    # Added models to the main user model (customized user)
    image = models.ImageField(upload_to='CustomUser/ImageUser/%y/%m/%d/', null=True, blank=True)  # image profile
    national_number = models.CharField(blank=True, default='-', max_length=10)
    card_number = models.CharField(blank=True, default='-', max_length=16)
    phone_number = models.CharField(blank=True, default='-', max_length=11)
    verify_code = models.CharField(blank=True, null=True, max_length=6)  # Verification code when sending email
