# Generated by Django 4.0.4 on 2022-09-12 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0075_alter_fieldofstudy_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldofstudy',
            name='title',
            field=models.CharField(choices=[('Software_Defined_Networking', 'شبکه و نرم افزار'), ('Mathematical_Physics', 'ریاضی فیزیک'), ('Experimental_Science', 'علوم تجربی'), ('Liberal_Arts', 'علوم انسانی')], max_length=50, verbose_name='عنوان رشته تحصیلی'),
        ),
    ]
