from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=50, choices=[('superadmin', 'superadmin'), ('admin', 'admin'), ('user', 'user')], default='superadmin')
    assigned_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)