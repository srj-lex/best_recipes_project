# Generated by Django 3.2.16 on 2023-08-27 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20230822_1133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingridient',
            old_name='units',
            new_name='measurement_unit',
        ),
    ]