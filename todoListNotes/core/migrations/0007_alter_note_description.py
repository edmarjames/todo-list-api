# Generated by Django 4.1.3 on 2023-03-02 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='description',
            field=models.TextField(default=''),
        ),
    ]