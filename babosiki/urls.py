import django
from django.urls import path
from django.views.generic import *
from .views import *

class Test(TemplateView):
    template_name = "home.html"
urlpatterns = [
    path('', OperationList.as_view(), name='operation_list'),
    path('d', DailyExpensesList.as_view(), name='operation_list'),
    path('a', AccountList.as_view(), name=''),
    path('load', MyView.as_view(), name=''),
    path('new/', OperationCreate.as_view(), name='operation_create'),
]