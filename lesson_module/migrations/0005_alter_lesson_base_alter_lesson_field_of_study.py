# Generated by Django 4.0.2 on 2022-05-06 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0015_alter_base_title_alter_fieldofstudy_title'),
        ('lesson_module', '0004_alter_lesson_base_alter_lesson_field_of_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='base',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.base', verbose_name='پایه2'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='field_of_study',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.fieldofstudy', verbose_name='رشته'),
        ),
    ]