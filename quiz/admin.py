from django.contrib import admin
from .models import Field,Question,Pin
# Register your models here.

admin.site.register(Field)
admin.site.register(Question)
admin.site.register(Pin)
# admin.site.register(Result)