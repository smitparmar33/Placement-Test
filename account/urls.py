from django.urls import path
from . import views
from .views import ResetPasswordView
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.site.site_header = "Welcome to Yudiz Placement Drive"
admin.site.site_title = "Yudiz Placement Drive"
admin.site.index_title = "Yudiz Placement Portal"

urlpatterns=[
    path('register',views.register,name='register'),
    path('',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
