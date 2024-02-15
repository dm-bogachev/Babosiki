# Generated by Django 3.2.24 on 2024-02-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babosiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Имя счёта')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='Комментарий')),
                ('initial_balance', models.FloatField(verbose_name='Начальный баланс')),
                ('type', models.CharField(choices=[(1, 'Дебетовый'), (-1, 'Кредитный')], max_length=32, verbose_name='Тип')),
                ('calculated', models.BooleanField(default=True, verbose_name='Используется в расчётах')),
            ],
            options={
                'verbose_name': 'Счета',
                'verbose_name_plural': 'Счёт',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
    ]
