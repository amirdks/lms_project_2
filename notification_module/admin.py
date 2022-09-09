from django.contrib import admin

from account_module.models import User
# Register your models here.
from notification_module.models import Notification, CustomNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['from_user', ]


@admin.register(CustomNotification)
class CustomNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'from_teacher']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'from_teacher':
            kwargs['queryset'] = User.objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
