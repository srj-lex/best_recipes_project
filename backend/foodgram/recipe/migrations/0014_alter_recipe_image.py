# Generated by Django 3.2.16 on 2023-09-14 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_auto_20230914_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=None, verbose_name='Изображение'),
        ),
    ]