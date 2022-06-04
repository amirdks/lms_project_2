from django.db import models

# Create your models here.
from account_module.models import User
from lesson_module.models import SetHomeWork


class Notification(models.Model):
    user = models.ManyToManyField(User, related_name='to_users', verbose_name='کاربران')
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE, verbose_name='از طرف')
    home_work = models.ForeignKey(SetHomeWork, null=True, blank=True, related_name='home_work',
                                  on_delete=models.CASCADE, verbose_name='مربوط به تکلیف')
    date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='زمان قرار گیری اعلان')
    time = models.TimeField(auto_now_add=True, blank=True, null=True, verbose_name='ساعت قرار کیری اعلان')
    text = models.TextField(verbose_name='متن اعلان')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان ها'

    def __str__(self):
        return self.from_user.get_full_name()

