from django.contrib import admin

# Register your models here.
from django.contrib import admin
from service.models import *
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import Tourist, SafetyLog

admin.site.register(Tourist)
admin.site.register(SafetyLog)

class ContactAdmin(admin.ModelAdmin):
    list_display=('username', 'email', 'add')


class FeedAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'msg')
admin.site.register(Feed, FeedAdmin)
    
# Register your models here.
