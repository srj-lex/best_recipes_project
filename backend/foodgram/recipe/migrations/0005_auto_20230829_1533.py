# Generated by Django 3.2.16 on 2023-08-29 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_rename_units_ingridient_measurement_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time',
            new_name='cooking_time',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
    ]
