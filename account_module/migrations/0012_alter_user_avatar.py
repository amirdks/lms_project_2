# Generated by Django 4.0.4 on 2022-09-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0011_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default-avatar/11-Azmayeshgah2.jpg', null=True, upload_to='images/profile', verbose_name='تصویر آواتار'),
        ),
    ]
