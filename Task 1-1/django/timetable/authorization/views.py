from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, CustomAdmin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from lessons.models import Teacher
from lessons.models import Group as lesson_Group
from lessons.views import create_group

# Create your views here.


def profile_teacher(request, teacher):
    groupsforinput = []
    for x in teacher.groups.all():
        groupsforinput.append(x.name)
    return render(request, 'profileTeacher.html', context={'user': teacher.user.user, 'groups': teacher.groups.all(),
                                                           'groupsAll': ' '.join(groupsforinput),
                                                           'subjects': teacher.subjects,
                                                           'role': teacher.user.user.groups.all()[0],
                                                           'photo': teacher.user.photo,
                                                           'realname': teacher.user.realname})


def profile(request, id):
    user = get_object_or_404(User, pk=id)

    teacher = Teacher.objects.filter(user__user=user)
    if len(teacher) > 0:
        teacher = teacher[0]
        return profile_teacher(request, teacher)

    try:
        custom = CustomUser.objects.get(user=user)
        realname = custom.realname
    except:
        custom = None
        realname = ""

    role = user.groups.all()
    if len(role) >= 1:
        role = role[0]
    else:
        role = None

    try:
        photo = custom.photo
    except:
        photo = None
    return render(request, 'profile.html', context={'user': user, 'photo': photo, 'role': role,
                                                    'realname': realname})


@user_passes_test(lambda user: user.is_superuser, login_url='/')
def change_profile(request, id):
    if request.method == "GET":
        return HttpResponseNotFound()
    user = get_object_or_404(User, pk=id)
    group, created = Group.objects.get_or_create(name=request.POST["role"])

    teachers = Teacher.objects.filter(user__user=user)
    for i in range(len(teachers)):
        teachers[i].delete()
    user.groups.clear()
    user.groups.add(group)

    custom = CustomUser.objects.filter(user=user)
    if len(custom) == 0:
        custom = CustomUser(user=user)
        custom.save()
    else:
        custom = custom[0]

    if str(group) == 'Преподаватель':
        teacher = Teacher(user=custom)
        teacher.save()
        if request.POST.get('groups', False):
            groups = request.POST['groups'].split(' ')
            teacher.groups.clear()

            for group in groups:
                res = create_group(group)
                teacher.groups.add(res)
        teacher.save()
    try:
        custom = CustomUser.objects.get(user=user)
        custom.realname = request.POST['realname']

        if request.FILES.get('photo', False):
            custom.photo = request.FILES['photo']
        custom.save()

    except:
        pass
    return redirect('/profile/' + str(id))


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            newCustomUser = CustomUser(user=form.instance)
            newCustomUser.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('/')
        return render(request, template_name='register.html', context={'form': form})

    return render(request, template_name='registration.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def loginView(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, template_name='login.html',
                          context={"errors": "User or password is not correct!"})

        login(request, user)
        return redirect('/')

    return render(request, template_name='login.html')


@login_required(redirect_field_name='/')
def logoutView(request):
    logout(request)
    return redirect('/')


class NewPassword(View):
    def get_user(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64, token)

        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'newPassword.html')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64, token)
        if user is not None and account_activation_token.check_token(user, token):
            if request.POST['password1'] != request.POST['password2']:
                return render(request, template_name='newPassword.html', context={'errors': 'passwords are not equal'})
            user.set_password(request.POST['password1'])
            user.save()
            return redirect('/')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def forgot_password(request):
    if request.method == 'POST':
        users = User.objects.filter(username=request.POST['username'], email=request.POST['email'])
        if len(users) == 0:
            return render(request, template_name='forgotPassword.html', context={'errors': 'User does not exists!'})
        elif len(users) > 1:
            return render(request, template_name='forgotPassword.html', context={'errors': 'User more than one!'})
        else:
            token = account_activation_token.make_token(users[0])
            print(token)
            print(users[0].id)
            return redirect('/newPassword/' + urlsafe_base64_encode(force_bytes(users[0].id)) + "/" + token)

    return render(request, template_name='forgotPassword.html')
