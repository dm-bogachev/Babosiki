from django.urls import path
from django.views.generic import RedirectView
from babosiki.views import *

urlpatterns = [
    path('', RedirectView.as_view(url='operation/list'), name='home'),
    #
    path('operation/transfer', OperationTransferFormView.as_view(), name='operation_transfer'),
    path('operation/list', OperationListView.as_view(), name='operation_list'),
    path('operation/create', OperationCreateView.as_view(), name='operation_create'),
    path('operation/edit/<int:pk>', OperationUpdateView.as_view(), name='operation_edit'),
    path('operation/delete/<int:pk>', OperationDeleteView.as_view(), name='operation_delete'),
    path('operation/list/<str:date>', OperationDailyListView.as_view(), name='operation_list_daily'),
    #
    path('category/list', CategoryListView.as_view(), name='category_list'),
    path('category/create', CategoryCreateView.as_view(), name='category_create'),
    path('category/edit/<int:pk>', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),
    #
    path('account/list', AccountListView.as_view(), name='account_list'),
    path('account/create', AccountCreateView.as_view(), name='account_create'),
    path('account/detail/<int:pk>', AccountDetailView.as_view(), name='account_detail'),
    path('account/edit/<int:pk>', AccountUpdateView.as_view(), name='account_edit'),
    path('account/delete/<int:pk>', AccountDeleteView.as_view(), name='account_delete'),
    #
    path('daily', DailyDeltaView.as_view(), name='daily'),
]