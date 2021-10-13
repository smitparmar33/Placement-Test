from django.contrib import admin
from .models import Student,College
# Register your models here.
class Filter(admin.ModelAdmin):
    list_filter = ("exam","college")

admin.site.register(Student,Filter)
admin.site.register(College)