from django.shortcuts import render, redirect
from .models import Lesson, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LessonForm
from django.db.models import F
from django.http import HttpResponse

# Create your views here.


def check_admin(user):
    return user.is_superuser


@user_passes_test(lambda user: user.is_superuser)
def add_lesson(request):
    if request.method == 'POST':
        d = {
            'title': request.POST['title'],
            'teacherName': request.POST['teacherName'],
            'beginTime': request.POST['beginTime'],
            'endTime': request.POST['endTime'],
            'link': request.POST['link'],
        }
        lesson = LessonForm(d)
        if not lesson.is_valid():
            return render(request, template_name='addLesson.html', context={'errors': "Error"})
        lesson.save()
        lesson = lesson.instance

        groups = request.POST['groups'].split(' ')
        for group in groups:
            try:
                g = Group.objects.get(name=group)
            except:
                newGroup = Group(name=group)
                newGroup.save()
                g = newGroup
            lesson.groups.add(g)

        return redirect('/timetable')

    return render(request, template_name='addLesson.html', context={'form': LessonForm})


@user_passes_test(lambda user: user.is_authenticated)
def timetable(request):
    class LessonWithGroup:
        def __init__(self, lessonModel):
            self.title = lessonModel.title
            self.beginTime = lessonModel.beginTime
            self.endTime = lessonModel.endTime
            self.teacherName = lessonModel.teacherName
            self.link = lessonModel.link
            self.groups = lessonModel.groups.all()

    lessons = []
    filtered = Lesson.objects.all()
    tags_all = {'All', 'Все'}
    if request.method == "POST":
        if request.POST['title'] and request.POST['title'] not in tags_all:
            filtered = filtered.filter(title=request.POST['title'])
        if request.POST['teacherName'] and request.POST['teacherName'] not in tags_all:
            filtered = filtered.filter(teacherName=request.POST['teacherName'])
        if request.POST['group'] and request.POST['group'] not in tags_all:
            filtered = filtered.filter(groups__name=request.POST['group'])

    for lesson in filtered:
        lessons.append(LessonWithGroup(lesson))

    return render(request, template_name='timetable.html', context={'lessons': lessons})
