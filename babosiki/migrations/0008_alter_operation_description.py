# Generated by Django 3.2.24 on 2024-02-15 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babosiki', '0007_alter_operation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='description',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Описание'),
        ),
    ]
