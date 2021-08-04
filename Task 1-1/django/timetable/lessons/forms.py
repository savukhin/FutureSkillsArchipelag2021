from django.contrib.auth.models import User
from .models import Lesson
from django.forms import ModelForm, Form
from django import forms


class LessonForm(ModelForm):
    # title = forms.CharField(max_length=200)
    # teacherName = forms.CharField(max_length=200)
    # beginTime = forms.DateTimeField()
    # endTime = forms.DateTimeField()
    # link = forms.CharField(max_length=200)

    # def __init__(self, *args, **kwargs):
    #     super(Lesson, self).__init__(*args, **kwargs)
    #     self.fields['title'].initial = kwargs.pop('title')
    #     self.fields['teacherName'].initial = kwargs.pop('teacherName')
    #     self.fields['beginTime'].initial = kwargs.pop('beginTime')
    #     self.fields['endTime'].initial = kwargs.pop('endTime')
    #     self.fields['link'].initial = kwargs.pop('link')
    #     self.fielsds['groups'].initial = kwargs.pop('groups')
    class Meta:
        model = Lesson
        fields = ['title', 'teacherName', 'beginTime', 'endTime', 'link']
