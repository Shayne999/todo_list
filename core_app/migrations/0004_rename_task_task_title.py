# Generated by Django 5.1.6 on 2025-02-11 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0003_task_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task',
            new_name='title',
        ),
    ]
