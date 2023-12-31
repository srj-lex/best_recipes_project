# Generated by Django 3.2.16 on 2023-09-04 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_auto_20230829_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngridientsForRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='ingridient',
            options={'ordering': ('name',), 'verbose_name': 'Ингридиент', 'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingridients',
        ),
        migrations.DeleteModel(
            name='IngridientAmount',
        ),
        migrations.AddField(
            model_name='ingridientsforrecipe',
            name='ingridient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.ingridient'),
        ),
        migrations.AddField(
            model_name='ingridientsforrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingridients',
            field=models.ManyToManyField(through='recipe.IngridientsForRecipe', to='recipe.Ingridient'),
        ),
    ]
