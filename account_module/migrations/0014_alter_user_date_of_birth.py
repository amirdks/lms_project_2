# Generated by Django 4.0.4 on 2022-09-21 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0013_user_address_user_date_of_birth_user_national_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
    ]