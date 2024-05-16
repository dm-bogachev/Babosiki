from django.db import models
from django.conf import settings
from django.utils import timezone


class Account(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',)

    name = models.CharField(max_length=32,
                            verbose_name='Имя счёта',)

    comment = models.CharField(max_length=128,
                               verbose_name='Комментарий',
                               blank=True,
                               null=True,)

    DEBIT = 1
    CREDIT = -1
    TYPES = (
        (DEBIT, "Дебетовый"),
        (CREDIT, "Кредитный"),)

    type = models.IntegerField(choices=TYPES,
                               verbose_name='Тип',)

    initial_balance = models.DecimalField(
        verbose_name='Начальный баланс', max_digits=25, decimal_places=2)

    calculated = models.BooleanField(default=True,
                                     verbose_name='Используется в расчётах',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Счёт'
        verbose_name = 'Счета'


class Operation(models.Model):

    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',)

    account = models.ForeignKey('Account',
                                on_delete=models.CASCADE,
                                verbose_name='Счёт',)

    INCOME = 1
    OUTCOME = -1
    TYPES = (
        (OUTCOME, "Расход"),
        (INCOME, "Пополнение"),)

    type = models.IntegerField(choices=TYPES,
                               verbose_name='Тип',)

    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 blank=True,
                                 null=True,)

    description = models.CharField(max_length=128,
                                   verbose_name='Описание',
                                   blank=True,
                                   null=True,)

    value = models.DecimalField(
        verbose_name='Сумма', max_digits=25, decimal_places=2)

    def __str__(self):
        return str(self.date) + ': ' + str(float(self.value)*int(self.type))

    class Meta:
        verbose_name_plural = 'Операции'
        verbose_name = 'Операция'
        ordering = ['date']


class Category(models.Model):
    name = models.CharField(max_length=32,
                            verbose_name='Название категории',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
