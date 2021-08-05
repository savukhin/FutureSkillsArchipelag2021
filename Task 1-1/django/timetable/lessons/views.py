from django.shortcuts import render, redirect
from .models import Lesson, Group, Subject, Teacher
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LessonForm
from django.db.models import F
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.


def check_admin(user):
    return user.is_superuser


def create_subject(title):
    if len(Subject.objects.filter(title=title)) > 0:
        return Subject.objects.get(title=title)
    subj = Subject(title=title)
    subj.save()
    return subj


def create_group(name):
    if len(Group.objects.filter(name=name)) > 0:
        return Group.objects.get(name=name)
    group = Group(name=name)
    group.save()
    return group



@user_passes_test(lambda user: user.is_superuser)
def add_lesson(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        subj = create_subject(request.POST['subject'])
        d = {
            'subject': subj,
            'teacherName': Teacher.objects.get(user__realname=request.POST['teacherName']),
            'beginTime': request.POST['beginTime'],
            'endTime': request.POST['endTime'],
            'link': request.POST['link'],
        }
        lesson = LessonForm(d)
        if not lesson.is_valid():
            return render(request, template_name='addLesson.html', context={'errors': lesson.errors,
                                                                            'subjects': subjects,
                                                                            'teachers': teachers
                                                                            })
        lesson.save()
        lesson = lesson.instance
        # lesson.subject = create_subject(d['subject'])

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

    return render(request, template_name='addLesson.html', context={'form': LessonForm, 'subjects': subjects,
                                                                    'teachers': teachers})


@user_passes_test(lambda user: user.is_authenticated)
def timetable(request):
    class LessonWithGroup:
        def __init__(self, lessonModel):
            self.title = lessonModel.subject.title
            self.beginTime = lessonModel.beginTime
            self.endTime = lessonModel.endTime
            self.teacherName = lessonModel.teacherName.user.realname
            self.link = lessonModel.link
            self.groups = lessonModel.groups.all()

    lessons = []
    filtered = Lesson.objects.all()
    tags_all = {'All', 'Все'}
    if request.method == "POST":
        if request.POST['title'] and request.POST['title'] not in tags_all:
            filtered = filtered.filter(subject__title=request.POST['title'])
        if request.POST['teacherName'] and request.POST['teacherName'] not in tags_all:
            filtered = filtered.filter(teacherName__user__realname=request.POST['teacherName'])
        if request.POST['group'] and request.POST['group'] not in tags_all:
            filtered = filtered.filter(groups__name=request.POST['group'])

    print(filtered)
    for lesson in filtered:
        lessons.append(LessonWithGroup(lesson))

    return render(request, template_name='timetable.html', context={'lessons': lessons})
