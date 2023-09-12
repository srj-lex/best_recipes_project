# Generated by Django 3.2.16 on 2023-09-06 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_auto_20230904_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingridients',
        ),
        migrations.AddField(
            model_name='recipe',
            name='text',
            field=models.TextField(default=str, max_length=500, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipe.Tag'),
        ),
        migrations.DeleteModel(
            name='IngridientsForRecipe',
        ),
    ]