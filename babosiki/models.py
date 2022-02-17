from django.db import models
from simple_history.models import HistoricalRecords


class Account(models.Model):
    history = HistoricalRecords()
    name = models.CharField(max_length=255,
                            verbose_name='Название счёта',)
    comment = models.CharField(max_length=255,
                               verbose_name='Комментарий',)
    value = models.FloatField(verbose_name='Баланс',)
    initial_value = models.FloatField(verbose_name='Начальный баланс',)
    # # For internal use
    no_d = models.IntegerField(default=0,
                               verbose_name='Количество дней',)

    def __str__(self) -> str:
        return self.name + ' (' + self.comment + ')'

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'


class OperationCategory(models.Model):
    history = HistoricalRecords()
    name = models.CharField(max_length=255,
                            verbose_name='Название',)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Operation(models.Model):
    history = HistoricalRecords()

    class OperationType(models.IntegerChoices):
        INCOME = 1, ('Доход')
        EXPENSES = -1, ('Расход')

    date = models.DateField(verbose_name='Дата',)
    type = models.IntegerField(choices=OperationType.choices,
                               verbose_name='Тип',)
    description = models.TextField(verbose_name='Описание',
                                   blank=True,)
    value = models.FloatField(verbose_name='Сумма',)
    repeatability = models.BooleanField(default=False,
                                        verbose_name='Повторяемый',)

    account = models.ForeignKey(to='Account',
                                verbose_name='Счёт',
                                on_delete=models.CASCADE,)

    category = models.ForeignKey(to='OperationCategory',
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE,)

    def __str__(self) -> str:
        return str(self.date) + ' - ' + self.description

    def save(self, *args, **kwargs):
        _date = self.date
        daily_expense = DailyExpenses.objects.filter(
            date=_date, account=self.account_id).first()
        if not daily_expense:
            account = Account.objects.get(pk=self.account_id)
            daily_expense = DailyExpenses(
                date=_date, value=self.type*self.value, account=account)
            daily_expense.save()
        super(Operation, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('date', 'description', 'value', 'account')
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class DailyExpenses(models.Model):
    history = HistoricalRecords()
    date = models.DateField(verbose_name='Дата',)
    value = models.FloatField(verbose_name='Сумма',)
    account = models.ForeignKey(to='Account',
                                verbose_name='Счёт',
                                on_delete=models.CASCADE,
                                null=True)

    # For internal use
    no_op = models.IntegerField(default=0,
                                verbose_name='Количество операций',)

    def __str__(self) -> str:
        return str(self.date)

    class Meta:
        unique_together = ('date', 'account',)
        verbose_name = 'Ежедневные расходы'
        verbose_name_plural = 'Ежедневные расходы'
