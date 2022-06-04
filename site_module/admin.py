from django.contrib import admin


# Register your models here.
from site_module.models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'is_main_setting']
    list_editable = ['is_main_setting']
