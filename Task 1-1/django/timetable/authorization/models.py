from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class CustomUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

@admin.register(CustomUser)
class CustomAdmin(admin.ModelAdmin):
    pass
