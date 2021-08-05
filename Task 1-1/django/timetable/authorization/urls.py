from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('changeProfile/<int:id>', views.change_profile, name='changeProfile'),

    path('forgotPassword', views.forgot_password, name='forgotPassword'),
    path('newPassword/<str:uidb64>/<str:token>',
                views.NewPassword.as_view(), name='activate_account'),
]
