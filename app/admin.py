from django.contrib import admin

# Register your models here.
from app.models import *

# project imports


class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "interval")
    search_fields = ("name",)
    readonly_fields = ("created_datetime",)


admin.site.register(Profile)
admin.site.register(Plan, PlanAdmin)
