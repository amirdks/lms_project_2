from django.contrib import admin
from . import models
from account_module.models import User


# Register your models here.


@admin.register(models.Lesson)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ['photo_tag', 'title', 'base', 'field_of_study', 'is_active']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['queryset'] = User.objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.SetHomeWork)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'teacher', 'get_reaming','poodeman_or_nobat','is_finished']


@admin.register(models.HomeWorks)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ['user', 'jalali_sent_at', 'home_work']


admin.site.register(models.HomeWorkFiles)
admin.site.register(models.PoodemanAndNobat)
