# Generated by Django 4.0.4 on 2022-09-24 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('send_email_module', '0004_alter_email_send_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name': 'ایمیل', 'verbose_name_plural': 'ایمیل ها'},
        ),
        migrations.AlterModelOptions(
            name='linkemailfile',
            options={'verbose_name': 'فایل ایمیل', 'verbose_name_plural': 'فایل های ایمیل'},
        ),
    ]