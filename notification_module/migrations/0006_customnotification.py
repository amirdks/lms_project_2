# Generated by Django 4.0.4 on 2022-09-07 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0072_alter_base_title'),
        ('notification_module', '0005_delete_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان اعلان')),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_base', to='lessons.base', verbose_name='برای پایه')),
                ('field_of_study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_field_of_study', to='lessons.fieldofstudy', verbose_name='برای رشته')),
                ('from_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_user', to=settings.AUTH_USER_MODEL, verbose_name='از طرف معلم')),
            ],
            options={
                'verbose_name': 'اعلان مخصوص',
                'verbose_name_plural': 'اعلانات مخصوص',
            },
        ),
    ]
