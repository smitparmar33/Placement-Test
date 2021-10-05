from django.contrib import admin
from .models import Student
# Register your models here.
class Filter(admin.ModelAdmin):
    list_filter = ("exam",)

admin.site.register(Student,Filter)