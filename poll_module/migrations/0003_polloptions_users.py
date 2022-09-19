# Generated by Django 4.0.4 on 2022-09-12 10:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll_module', '0002_rename_active_poll_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='polloptions',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='poll_option_user', to=settings.AUTH_USER_MODEL, verbose_name='کاربران'),
        ),
    ]