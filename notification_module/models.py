import jalali_date
from django.db import models

# Create your models here.
from account_module.models import User
from lesson_module.models import SetHomeWork
from utils.convertors import change_month, persian_number_converter


class Notification(models.Model):
    user = models.ManyToManyField(
        'account_module.User',
        related_name='to_users',
        verbose_name='کاربران'
    )
    from_user = models.ForeignKey(
        'account_module.User',
        related_name='from_user',
        on_delete=models.CASCADE,
        verbose_name='از طرف'
    )
    home_work = models.ForeignKey(
        'lesson_module.SetHomeWork',
        null=True,
        blank=True,
        related_name='home_work',
        on_delete=models.CASCADE,
        verbose_name='مربوط به تکلیف'
    )
    date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='زمان قرار گیری اعلان'
    )
    time = models.TimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='ساعت قرار کیری اعلان'
    )
    text = models.TextField(
        verbose_name='متن اعلان'
    )

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان ها'

    def __str__(self):
        return self.from_user.get_full_name()


class CustomNotification(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='عنوان اعلان'
    )
    text = models.TextField(
        verbose_name='متن اعلان',
        blank=True,
        null=True,
    )
    from_teacher = models.ForeignKey(
        'account_module.User',
        on_delete=models.CASCADE,
        verbose_name='از طرف معلم',
        related_name='notification_user'
    )
    base = models.ForeignKey(
        'lessons.Base',
        verbose_name='برای پایه',
        on_delete=models.CASCADE,
        related_name='notification_base'
    )
    field_of_study = models.ForeignKey(
        'lessons.FieldOfStudy',
        verbose_name='برای رشته',
        on_delete=models.CASCADE,
        related_name='notification_field_of_study'
    )
    publish = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ساخت",
    )

    class Meta:
        verbose_name = 'اعلان مخصوص'
        verbose_name_plural = 'اعلانات مخصوص'

    def __str__(self):
        return self.title

    def jalali_publish(self):
        return persian_number_converter(change_month(jalali_date.datetime2jalali(self.publish).strftime('%Y/%m/%d')))
