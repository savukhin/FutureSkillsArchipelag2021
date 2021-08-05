from django.db import models
# from authorization.models import Teacher
from authorization.models import CustomUser

# Create your models here.


class Subject(models.Model):
    title = models.CharField(max_length=200)


class Group(models.Model):
    name = models.CharField(max_length=30)


class Teacher(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    subjects = models.ManyToManyField(Subject)


class Lesson(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    beginTime = models.DateTimeField()
    endTime = models.DateTimeField()
    teacherName = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)
