# Generated by Django 3.2.16 on 2023-09-20 09:09

from django.db import migrations, models
import user.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20230829_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[user.validators.validate_username], verbose_name='Псевдоним пользователя'),
        ),
    ]
