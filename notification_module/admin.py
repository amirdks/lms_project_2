from django.contrib import admin

# Register your models here.
from notification_module.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['from_user', ]


