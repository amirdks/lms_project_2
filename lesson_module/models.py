from django.db import models

from datetime import datetime

from django.utils.html import format_html
from jalali_date import datetime2jalali

from lessons.models import Base, FieldOfStudy

# Create your models here.
from account_module.models import User
from utils.time import end_time_reaming


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان درس')
    image = models.ImageField(upload_to='images/lessons', verbose_name='عکس درس')
    base = models.ForeignKey(to=Base, null=True, blank=True, on_delete=models.CASCADE, verbose_name='پایه')
    field_of_study = models.ForeignKey(to=FieldOfStudy, null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='رشته')
    teacher = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='معلم')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    def __str__(self):
        return f'درس {self.title} -  {self.base.title_farsi()} - رشته {self.field_of_study.title_farsi()}'

    def photo_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.image.url))

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس ها"

    photo_tag.short_description = 'تصویر درس'


class SetHomeWork(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان تکلیف')
    start_at = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='تاریخ ثبت تکلیف')
    end_at = models.DateTimeField(verbose_name='تاریخ پایان مهلت تکلیف')
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, verbose_name='مربوط به درس')
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, editable=True, verbose_name='معلم')
    description = models.TextField(verbose_name='توضیحات تکلیف')
    is_finished = models.BooleanField(default=False, verbose_name='به اتمام رسیده')

    def __str__(self):
        return self.title

    def get_reaming(self):
        return end_time_reaming(self.end_at)

    class Meta:
        verbose_name = "تکلیف قرار داده شده"
        verbose_name_plural = 'تکالیف قرار داده شده'

    get_reaming.short_description = 'زمان باقیمانده'


class HomeWorks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='دانش آموز')
    send_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    home_work = models.ForeignKey(to=SetHomeWork, on_delete=models.CASCADE, related_name='taklif',
                                  verbose_name='مربوط به تکلیف')
    file = models.FileField(upload_to='files/home_works', verbose_name='تکلیف ارسال شده')
    is_delivered = models.BooleanField(default=False, verbose_name='وضعیت تحویل')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'تکلیف ارسال شده'
        verbose_name_plural = 'تکالیف ارسال شده'

    def user_name(self):
        return self.user.username

    def jalali_sent_at(self):
        return datetime2jalali(self.send_at).strftime("%m/%d/%Y %H:%M:%S")

    jalali_sent_at.short_description = 'زمان ارسال'
