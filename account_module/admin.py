from django.contrib import admin
# Register your models here.
from django.utils.crypto import get_random_string

from account_module.models import User


# from lessons.models import Lessons

def make_is_teacher(modeladmin, request, queryset):
    for user in queryset:
        if user.is_teacher:
            queryset.update(is_teacher=False)
        else:
            queryset.update(is_teacher=True)


make_is_teacher.short_description = 'تبدیل به معلم'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','photo_tag',  'last_name', 'first_name', 'base', 'field_of_study', 'is_teacher']
    list_editable = ['base', 'field_of_study']
    list_filter = ['is_teacher', 'base', 'field_of_study']
    ordering = ['is_teacher', 'base', 'field_of_study']
    actions = [make_is_teacher]

    def save_model(self, request, obj: User, form, change):
        if change is False:
            obj.email_active_code = get_random_string(72)
            password = form.cleaned_data.get('password')
            obj.set_password(password)

        return super(UserAdmin, self).save_model(request, obj, form, change)
