from django.db import models
from django.utils.html import format_html
from jalali_date import datetime2jalali
from pathlib import Path
# Create your models here.
from account_module.models import User
from lessons.models import Base, FieldOfStudy, AllowedFormats
from utils.time import end_time_reaming


class Lesson(models.Model):
    POODEMAN_OR_NOBAT = [
        ("poodeman", "پودمانی"),
        ("nobat", "نوبتی"),
    ]
    title = models.CharField(max_length=50, verbose_name='عنوان درس')
    image = models.ImageField(upload_to='images/lessons', verbose_name='عکس درس')
    base = models.ForeignKey(to=Base, null=True, blank=True, on_delete=models.CASCADE, verbose_name='پایه')
    field_of_study = models.ForeignKey(to=FieldOfStudy, null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='رشته')
    teacher = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='معلم')
    poodeman_or_nobat = models.CharField(choices=POODEMAN_OR_NOBAT, default='poodeman', max_length=20,
                                         verbose_name='نوع درس')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    def __str__(self):
        return f'درس {self.title} -  {self.base.title_farsi()} - رشته {self.field_of_study.title_farsi()}'

    def photo_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.image.url))

    def type_farsi(self):
        if self.poodeman_or_nobat == 'poodeman':
            return "پودمان"
        return "نوبت"

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
    max_size = models.FloatField(blank=True, null=True, verbose_name='حداکثر اندازه فایل(mb)')
    allowed_formats = models.ManyToManyField(to=AllowedFormats, related_name='allowed_formats', blank=True,
                                             verbose_name='فرمت های مجاز')
    poodeman_or_nobat = models.ForeignKey(to='PoodemanAndNobat', null=True, blank=True, on_delete=models.CASCADE,
                                          verbose_name='پودمان یا نوبت')
    score_weight = models.PositiveIntegerField(null=True, blank=True, verbose_name='وزن نمره')
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
    message = models.TextField(blank=True, null=True, verbose_name='پیام به معلم')
    score = models.FloatField(null=True, blank=True, verbose_name='نمره تکلیف')
    score_percent = models.FloatField(max_length=100, null=True, blank=True,verbose_name='درصد نمره')
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

    def is_score_ok(self):
        if self.score > self.home_work.score_weight:
            return False
        return True

    def score_percent_func(self):
        return self.score * 100 / self.home_work.score_weight

    jalali_sent_at.short_description = 'زمان ارسال'


class HomeWorkFiles(models.Model):
    home_work = models.ForeignKey(to='HomeWorks', on_delete=models.CASCADE, verbose_name='مربوط به تکلیف')
    file = models.FileField(upload_to='files/home_works', verbose_name='فایل تکلیف')

    def __str__(self):
        return Path(self.file.name).stem

    class Meta:
        verbose_name = 'فایل ارسال شده'
        verbose_name_plural = 'فایل های ارسال شده'


class PoodemanAndNobat(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام')
    type = models.CharField(max_length=15, choices=[("poodeman", "پودمانی"),
                                                    ("nobat", "نوبتی"), ], verbose_name='نوع')
    slug = models.SlugField(unique=True, max_length=30, blank=True, null=True, verbose_name='عنوان در url')

    def __str__(self):
        return self.name

    def type_farsi(self):
        if self.type == 'poodeman':
            return "پودمان"
        return "نوبت"

    class Meta:
        verbose_name = 'پودمان و نوبت'
        verbose_name_plural = 'پودمان ها و نوبت ها'
