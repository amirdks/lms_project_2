from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite

from . import models
from .models import AllowedFormats


@admin.register(models.Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = ['title', ]

    def save_model(self, request, obj: models.Base, form, change):
        if change is False:
            if form.cleaned_data.get('paye_10'):
                obj.base_number = 10
            elif form.cleaned_data.get('paye_11'):
                obj.base_number = 11
            else:
                obj.base_number = 12
        return super().save_model(request, obj, form, change)


@admin.register(models.FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ['title', ]


admin.site.register(AllowedFormats)
