from django.contrib import admin
# Register your models here.
from django.utils.crypto import get_random_string
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from account_module.models import User


# from lessons.models import Lessons

def make_is_teacher(modeladmin, request, queryset):
    for user in queryset:
        if user.is_teacher:
            queryset.update(is_teacher=False)
        else:
            queryset.update(is_teacher=True)


make_is_teacher.short_description = 'تبدیل به معلم'


def make_base_and_fieldofstudy(modeladmin, request, queryset):
    for user in queryset:
        queryset.update(base_id=1, field_of_study_id=3)


make_base_and_fieldofstudy.short_description = 'تغییر به پایه ده و رشته کامپیوتر'


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'photo_tag', 'last_name', 'first_name', 'base', 'field_of_study', 'is_teacher']
#     list_filter = ['is_teacher', 'base', 'field_of_study']
#     ordering = ['is_teacher', 'base', 'field_of_study']
#     actions = [make_is_teacher, make_base_and_fieldofstudy]
#
#     def save_model(self, request, obj: User, form, change):
#         if change is False:
#             obj.email_active_code = get_random_string(72)
#             password = form.cleaned_data.get('password')
#             obj.set_password(password)
#
#         return super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    # show jalali date in list display
    list_display = ['username', 'photo_tag', 'last_name', 'first_name', 'base', 'field_of_study', 'is_teacher']

    list_filter = ['is_teacher', 'base', 'field_of_study']

    ordering = ['is_teacher', 'base', 'field_of_study']
    actions = [make_is_teacher, make_base_and_fieldofstudy]

    # you can override formfield, for example:

    def get_jalali_date_of_birth(self, obj):
        return datetime2jalali(obj.date_of_birth).strftime('%y/%m/%d')

    def save_model(self, request, obj: User, form, change):
        if change is False:
            obj.email_active_code = get_random_string(72)
            password = form.cleaned_data.get('password')
            obj.set_password(password)

        return super(UserAdmin, self).save_model(request, obj, form, change)

    get_jalali_date_of_birth.short_description = 'تاریخ تولد'
    get_jalali_date_of_birth.admin_order_field = 'date_of_birth'
