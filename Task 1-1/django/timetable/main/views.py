from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return redirect('/timetable')
    return render(request, template_name='index.html')
