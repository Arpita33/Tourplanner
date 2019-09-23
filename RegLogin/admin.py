from django.contrib import admin
from .models import PROFILE
from django.contrib.auth.models import User

class PROFILEAdmin(admin.ModelAdmin):
    list_display = ['id', 'Address', 'Phone', 'image_tag', 'about', 'gender', 'is_Guide']


admin.site.register(PROFILE, PROFILEAdmin)
# Register your models here.
