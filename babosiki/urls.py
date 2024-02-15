from django.urls import path
from babosiki.views import *

urlpatterns = [
    path('', AccountListView.as_view(), name='home'),
    path('transfer', TransferFormView.as_view(), name='transfer'),
    path('operations', OperationsListView.as_view(), name='operations'),
    path('operations/add', AddOperationView.as_view(), name='add_operation'),
    path('operations_day/<str:date>', DayListView.as_view(), name='operations_day'),
    path('daily', DaysListView.as_view(), name='daily'),
]