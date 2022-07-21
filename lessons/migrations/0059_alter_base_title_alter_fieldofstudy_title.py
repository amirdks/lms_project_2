# Generated by Django 4.0.4 on 2022-06-26 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0058_alter_base_title_alter_fieldofstudy_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='title',
            field=models.CharField(choices=[('paye_11', 'پایه یازدهم'), ('paye_12', 'پایه دوازدهم'), ('paye_10', 'پایه دهم')], default='paye_10', max_length=50, verbose_name='عنوان پایه'),
        ),
        migrations.AlterField(
            model_name='fieldofstudy',
            name='title',
            field=models.CharField(choices=[('Software_Defined_Networking', 'شبکه و نرم افزار'), ('Mathematical_Physics', 'ریاضی فیزیک'), ('Experimental_Science', 'علوم تجربی'), ('Liberal_Arts', 'علوم انسانی')], max_length=50, verbose_name='عنوان رشته تحصیلی'),
        ),
    ]
