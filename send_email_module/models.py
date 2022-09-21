from django.db import models


# Create your models here.

class Email(models.Model):
    subject = models.CharField(
        max_length=50,
        verbose_name='موضوع ایمیل',
    )
    content = models.TextField(
        verbose_name='متن ایمیل'
    )
    from_teacher = models.ForeignKey(
        'account_module.User',
        verbose_name='از طرف معلم',
        on_delete=models.CASCADE,
        related_name='email_sender'
    )
    base = models.ForeignKey(
        'lessons.Base',
        on_delete=models.CASCADE,
        verbose_name='برای به پایه',
        related_name='email_base'
    )
    field_of_study = models.ForeignKey(
        'lessons.FieldOfStudy',
        on_delete=models.CASCADE,
        verbose_name='برای به رشته',
        related_name='email_field_of_study',
    )
    send_at = models.DateTimeField(
        verbose_name='ارسال در تاریخ',
        auto_now_add=True
    )


class LinkEmailFile(models.Model):
    email = models.ForeignKey('Email', on_delete=models.CASCADE, verbose_name='برای ایمیل')
    file = models.FileField(
        upload_to='files/email'
    )
