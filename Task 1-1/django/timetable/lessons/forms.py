from django.contrib.auth.models import User
from .models import Lesson
from django.forms import ModelForm, Form
from django import forms


class LessonForm(ModelForm):
    # subject = forms.CharField()

    class Meta:
        model = Lesson
        fields = ['subject', 'teacherName', 'beginTime', 'endTime', 'link']
