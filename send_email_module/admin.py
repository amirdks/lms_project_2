from django.contrib import admin

from send_email_module.models import Email, LinkEmailFile


# Register your models here.
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'from_teacher', 'base', 'field_of_study']


@admin.register(LinkEmailFile)
class LinkEmailFileAdmin(admin.ModelAdmin):
    list_display = ['email']
