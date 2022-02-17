import django
from django.urls import path
from django.views.generic import *
from .views import *

urlpatterns = [
    path('operation/list', OperationList.as_view(), name='operation_list'),
    path('', OperationList.as_view(), name=''),
    path('dailyexpenses/list', DailyExpensesList.as_view(), name='dailyexpenses_list'),
    path('account/list', AccountList.as_view(), name='account_list'),
    path('load', MyView.as_view(), name=''),
    path('operation/create', OperationCreate.as_view(), name='operation_create'),
]