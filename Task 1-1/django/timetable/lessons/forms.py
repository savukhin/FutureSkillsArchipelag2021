from django.contrib.auth.models import User
from .models import Lesson
from django.forms import ModelForm, Form
from django import forms


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'teacherName', 'beginTime', 'endTime', 'link']
