from cmath import nan
from dataclasses import fields
import datetime
import re
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *


def update_daily_expenses():
    # Update only if there were any changes
    daily_expenses = DailyExpenses.objects.all()
    for item in daily_expenses:
        operations = Operation.objects.filter(
            date=item.date, account=item.account)
        if item.no_op != len(operations):
            value = 0
            for operation in operations:
                value += operation.value*operation.type
            item.value = value
            item.no_op = len(operations)
            item.save()


def update_accounts():
    # Update only if there were any changes
    accounts = Account.objects.all()
    for item in accounts:
        daily_expenses = DailyExpenses.objects.filter(account=item.id)
        value = 0
        for daily_expense in daily_expenses:
            value += daily_expense.value
        item.value = value + item.initial_value
        item.no_d = len(daily_expenses)
        item.save()


class DailyExpensesList(ListView):
    model = DailyExpenses

    def get_context_data(self, **kwargs):
        update_daily_expenses()
        context = super(DailyExpensesList, self).get_context_data(**kwargs)
        return context


class AccountList(ListView):
    model = Account

    def get_context_data(self, **kwargs):
        update_daily_expenses()
        update_accounts()
        context = super(AccountList, self).get_context_data(**kwargs)
        return context


class OperationList(ListView):
    model = Operation
    ordering = ['-date']


class OperationCreate(CreateView):
    model = Operation
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('operation_list')

class OperationUpdate(UpdateView):
    model = Operation
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('operation_list')

class MyView(View):

    def load_data(self):
        xl = pd.ExcelFile(
            r'C:\Users\dmbog\Программирование\Проекты\Babosiki\nodjango\money.xlsx')
        xl = xl.parse(2)
        for value in xl.values:
            try:
                type = value[2]
                date = value[0]
                category = value[3]
                description = value[5]
                repeat = value[4]
                if repeat is not True:
                    repeat = False
                account_id = value[1]
                val = value[6]
    ##
                account = Account.objects.get(pk=account_id)
                #date = datetime.datetime.fromtimestamp(date).date()
                cat = OperationCategory.objects.filter(name=category).first()
                if not cat:
                    cat = OperationCategory(name=category)
                    cat.save()
                operation = Operation(date=date, type=type, description=description,
                                    value=val, account=account, repeatability=repeat,
                                    category=cat)

                operation.save()
                daily_expense = DailyExpenses.objects.filter(
                    date=date, account=account_id).first()
                if not daily_expense:
                    account = Account.objects.get(pk=account_id)
                    daily_expense = DailyExpenses(
                        date=date, value=type*val, account=account)
                    daily_expense.save()
                    pass
            except Exception:
                pass
        pass

    def get(self, request, *args, **kwargs):
        self.load_data()
        return HttpResponse('Hello, World!')
