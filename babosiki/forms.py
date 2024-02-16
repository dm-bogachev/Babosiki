from django import forms
from django.utils import timezone


from .models import Account, Operation, Category

class TransferForm(forms.Form):

    date = forms.DateField(initial=timezone.now,
                           label='Дата')

    source = forms.ModelChoiceField(queryset=Account.objects.all(),
                                    empty_label='Исходный счёт',
                                    label='Исходный счёт',)
    target = forms.ModelChoiceField(queryset=Account.objects.all(),
                                    empty_label='Целевой счёт',
                                    label='Целевой счёт',)
    value = forms.FloatField(min_value=0.0,
                             label='Сумма',)
    
    def transfer(self):
        date = self.data['date']
        date = date.split('.')
        date = '-'.join([date[2], date[1], date[0]])
        source_pk = self.data['source']
        target_pk = self.data['target']
        value = float(self.data['value'])
        source_operation_account = Account.objects.get(pk=source_pk)
        target_operation_account = Account.objects.get(pk=target_pk)


        source_operation = Operation()
        source_operation.date = date
        source_operation.account = source_operation_account
        source_operation.type = source_operation.OUTCOME
        source_operation.category = Category.objects.first()
        source_operation.description = 'Перевод со счёта {} на счёт {}'.format(source_operation_account, 
                                                                               target_operation_account)
        source_operation.value = value
        source_operation.save()

        target_operation = Operation()
        target_operation.date = date
        target_operation.account = target_operation_account
        target_operation.type = target_operation.INCOME
        target_operation.category = Category.objects.first()
        target_operation.description = 'Перевод со счёта {} на счёт {}'.format(source_operation_account, 
                                                                               target_operation_account)
        target_operation.value = value
        target_operation.save()
    