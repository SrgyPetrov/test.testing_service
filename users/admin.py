from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(BaseUserAdmin):

    pass


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
