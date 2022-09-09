from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html
from lessons.models import Base, FieldOfStudy


class User(AbstractUser):
    email = models.EmailField(verbose_name="email address", unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/profile',
                               default='default-avatar/11-Azmayeshgah2.jpg', verbose_name='تصویر آواتار')
    email_active_code = models.CharField(blank=True, null=True, editable=False, max_length=100,
                                         verbose_name='فعالسازی ایمیل')
    base = models.ForeignKey(Base, blank=True, null=True, on_delete=models.CASCADE, verbose_name='پایه دانش آموز')
    field_of_study = models.ForeignKey(FieldOfStudy, blank=True, null=True, on_delete=models.CASCADE,
                                       verbose_name='رشته')
    is_teacher = models.BooleanField(default=False, verbose_name='معلم')

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = 'کاربران'

    def photo_tag(self):
        if self.avatar:
            photo_tag = format_html(
                "<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.avatar.url))
        else:
            photo_tag = format_html("""کاربر پروفایلی ندارد""")
        return photo_tag

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        elif self.email != '':
            return self.email
        else:
            return self.username

    photo_tag.short_description = 'پروفایل کاربر'
