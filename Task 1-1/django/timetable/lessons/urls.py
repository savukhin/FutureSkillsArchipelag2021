from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('timetable', views.timetable, name='timetable'),
    path('addLesson', views.add_lesson, name='addLesson'),
]
