# Generated by Django 4.0.4 on 2022-09-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send_email_module', '0003_alter_email_send_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='send_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='ارسال در تاریخ'),
        ),
    ]
