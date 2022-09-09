# Generated by Django 4.0.4 on 2022-09-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0071_alter_base_title_alter_fieldofstudy_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='title',
            field=models.CharField(choices=[('paye_10', 'پایه دهم'), ('paye_11', 'پایه یازدهم'), ('paye_12', 'پایه دوازدهم')], default='paye_10', max_length=50, verbose_name='عنوان پایه'),
        ),
    ]
