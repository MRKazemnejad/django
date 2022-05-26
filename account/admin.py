from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

class UserInline(admin.StackedInline):
    model = Profile

class UserAdmin(BaseUserAdmin):
    inlines=(UserInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
