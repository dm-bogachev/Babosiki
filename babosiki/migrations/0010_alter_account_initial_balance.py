# Generated by Django 3.2.24 on 2024-05-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babosiki', '0009_auto_20240516_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='initial_balance',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Начальный баланс'),
        ),
    ]
