from django.urls import path
from . import views
from django.contrib import admin

# admin customizations
admin.site.site_header = "Welcome to Yudiz Placement Drive"
admin.site.site_title = "Yudiz Placement Drive"
admin.site.index_title = "Yudiz Placement Portal"

urlpatterns=[
    path('register',views.register,name='register'),
    path('',views.login,name='login'),
    path('logout',views.logout,name='logout'),
]
