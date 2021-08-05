from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
# from lessons.models import Group

# Create your models here.


class CustomUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/userphoto', blank=True)
    realname = models.CharField(max_length=200, default="Неизвестно", null=False)


@admin.register(CustomUser)
class CustomAdmin(admin.ModelAdmin):
    pass
