from django.contrib import admin
from .models import Field,Question,Pin
# Register your models here.
# admin.site.register(Result)
class Filter(admin.ModelAdmin):
    list_filter = ("field",)

admin.site.register(Question, Filter)
admin.site.register(Field)
admin.site.register(Pin)
