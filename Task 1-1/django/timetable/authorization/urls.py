from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.loginView, name='login'),

    path('forgotPassword', views.forgot_password, name='forgotPassword'),
    # url(r'^password/change/$', views.PasswordChangeView.as_view(), name='password_change'),
    # url(r'^password/change/done/$', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # url(r'^password/reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password/reset/done/$', views.PasswordResetDoneView.as_view(),  name='password_reset_done'),
    # url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #
    # url(r'^password/reset/complete/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
# </token></uidb64>
