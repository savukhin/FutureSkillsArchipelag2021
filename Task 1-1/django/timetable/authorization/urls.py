from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    # path('accounts/login/', views.loginView, name='accounts_login'),

    path('forgotPassword', views.forgot_password, name='forgotPassword'),
    # url(r'^newPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #             views.NewPassword.as_view(), name='activate_account'),
    # url(r'^newPassword/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #             views.NewPassword.as_view(), name='activate_account')
    path('newPassword/<str:uidb64>/<str:token>',
                views.NewPassword.as_view(), name='activate_account'),
    # url(r'^accounts/login/$', auth_views.LoginView.as_view(), name="asdfasdflogin"),
    # url(r'^password/change/$', auth_views.PasswordChangeView.as_view(
    #     template_name="authorization/templates/password_change.html"), name='password_change'),
    # url(r'^password/change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # url(r'^password/reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'),
    #
    # url(r'^password/reset/complete/$',
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name='password_reset_complete'),
]
# </token></uidb64>
