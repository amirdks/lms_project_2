from django.db import models


# Create your models here.

class Poll(models.Model):
    question = models.CharField(
        max_length=30,
        verbose_name='عنوان سوال',
    )
    from_teacher = models.ForeignKey(
        'account_module.User',
        verbose_name='از طرف معلم',
        on_delete=models.CASCADE,
        related_name='poll_teacher'
    )
    users = models.ManyToManyField(
        'account_module.User',
        related_name='poll_user',
        blank=True,
        verbose_name='کاربران',
    )
    base = models.ForeignKey(
        verbose_name='برای پایه',
        to='lessons.Base',
        on_delete=models.CASCADE,
        related_name='poll_base'
    )
    field_of_study = models.ForeignKey(
        verbose_name='برای رشته',
        to='lessons.FieldOfStudy',
        on_delete=models.CASCADE,
        related_name='poll_fieldofstudy'
    )
    create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ساخت',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال / غیرفعال',
    )

    # Metadata
    class Meta:
        verbose_name = 'نظرسنجی'
        verbose_name_plural = 'نظرسنجی ها'
        ordering = ('-create',)

    # Methods
    def __str__(self):
        return self.question

    @property
    def all_count(self):
        polls = Poll.objects.all().count()
        return polls


class PollOptions(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='poll_option',
        verbose_name='برای نظرسنجی',
    )
    option = models.CharField(
        max_length=30,
        verbose_name='گزینه',
    )
    option_count = models.IntegerField(
        default=0,
        verbose_name='شمارش گزینه',
    )

    # Metadata
    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه ها'

    # Methods
    def __str__(self):
        return self.option
