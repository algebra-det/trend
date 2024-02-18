from django.contrib import admin
from .models import MyUser, Code

from django.contrib.auth.models import Group

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'id', 'first_name', 'last_name', 'province', 'is_verified', 'is_admin']
    search_fields = ['email', 'first_name', 'last_name', 'province']


admin.site.unregister(Group)


@admin.register(Code)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'usage', 'confirmation_code']
    search_fields = ['email', 'created_at']