from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=30)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    beginTime = models.DateTimeField()
    endTime = models.DateTimeField()
    teacherName = models.CharField(max_length=200)
    link = models.CharField(max_length=200)


class GroupLessonRel(models.Model):
    group = models.OneToOneField(to=Group, on_delete=models.CASCADE)
    lesson = models.OneToOneField(to=Lesson, on_delete=models.CASCADE)