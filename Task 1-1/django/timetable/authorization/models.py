from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

@admin.register
class CustomAdmin(admin.ModelAdmin):
    pass


class CustomUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
