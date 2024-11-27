from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    otp_created_time = models.DateTimeField(default=timezone.now)
    otp_expiry_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.otp_expiry_time = self.otp_created_time + timedelta(minutes=2)  # Set expiry time to 2 minutes
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
