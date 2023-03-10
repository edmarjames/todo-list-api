# Generated by Django 4.1.3 on 2023-03-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='activate_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='deactivate_date',
        ),
        migrations.AddField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
