# Generated by Django 4.1.3 on 2023-03-02 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_note_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='activate_date',
        ),
        migrations.RemoveField(
            model_name='note',
            name='deactivate_date',
        ),
        migrations.RemoveField(
            model_name='note',
            name='status',
        ),
    ]