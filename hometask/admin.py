from django.contrib import admin
from hometask.models import Hometask
@admin.register(Hometask)
class HometaskAdmin(admin.ModelAdmin):
    pass