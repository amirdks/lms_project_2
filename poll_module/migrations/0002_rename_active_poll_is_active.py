# Generated by Django 4.0.4 on 2022-09-09 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll_module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='active',
            new_name='is_active',
        ),
    ]