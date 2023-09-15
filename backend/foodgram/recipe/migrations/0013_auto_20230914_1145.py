# Generated by Django 3.2.16 on 2023-09-14 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_auto_20230909_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Корзина покупок', 'verbose_name_plural': 'Корзина покупок'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, upload_to=None, verbose_name='Изображение'),
        ),
    ]
