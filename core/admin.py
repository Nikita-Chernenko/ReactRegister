from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User

class CoreAdmin(UserAdmin):
    UserAdmin.list_display += ('staff',)
    UserAdmin.list_filter += ('staff',)
    UserAdmin.fieldsets += (('staff', {'fields': ('staff',)}),)
admin.site.register(User, CoreAdmin)