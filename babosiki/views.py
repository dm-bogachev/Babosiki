from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.urls import reverse_lazy
from babosiki.forms import * 

class OperationTransferFormView(LoginRequiredMixin, FormView ):
    template_name = 'operation_transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('operation_list')

    def form_valid(self, form):
        form.transfer()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = Account.objects.filter(user=self.request.user)
        context['form'].fields['source'].queryset = accounts
        context['form'].fields['target'].queryset = accounts
        #
        return context

class OperationListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "operation_list.html"

    def get_context_data(self, **kwargs):
        accounts = Account.objects.filter(user=self.request.user)
        operations = Operation.objects.filter(account__id__in=accounts.all())
        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        return context
    

class OperationDailyListView(LoginRequiredMixin, TemplateView):
    
    login_url = 'login'
    
    template_name = "operation_daily_list.html"

    def get_context_data(self, **kwargs):
        date = self.kwargs.get('date', None)
        accounts = Account.objects.filter(user=self.request.user, calculated=True)
        operations = Operation.objects.filter(date=date, account__id__in=accounts.all())
        delta = 0.0
        for operation in operations:
            delta += operation.value*operation.type

        accounts = Account.objects.filter(user=self.request.user)
        operations = Operation.objects.filter(date=date, account__id__in=accounts.all())
        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        context['delta'] = delta
        return context
    

class OperationCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    
    model = Operation
    fields = '__all__'

    template_name = 'operation_create.html'

    def __init__(self):
        super(OperationCreateView, self).__init__()

    def get_success_url(self):
        return reverse_lazy('operation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OperationCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = Account.objects.filter(user=self.request.user)
        context['form'].fields['account'].queryset = accounts
        #
        return context

class OperationUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Operation
    fields = '__all__'

    template_name = 'operation_create.html'

    def __init__(self):
        super(OperationUpdateView, self).__init__()

    def get_success_url(self):
        return reverse_lazy('operation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OperationUpdateView, self).form_valid(form)


class OperationDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    
    model = Operation

    template_name = 'operation_delete.html'

    def __init__(self):
        super(OperationDeleteView, self).__init__()

    def get_success_url(self):
        return reverse_lazy('operation_list')


class CategoryListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    
    model = Category
    template_name = 'category_list.html'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    
    model = Category
    fields = '__all__'
    template_name = 'category_create.html'

    def get_success_url(self):
        return reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Category
    fields = '__all__'
    template_name = 'category_create.html'

    def get_success_url(self):
        return reverse_lazy('category_list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    
    model = Category
    template_name = 'category_delete.html'

    def get_success_url(self):
        return reverse_lazy('category_list')


class AccountListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    
    template_name = "account_list.html"

    def get_context_data(self, **kwargs):
        accounts= Account.objects.filter(user=self.request.user)
        account_values = {}
        for account in accounts:
            operations = Operation.objects.filter(account=account)
            total_sum = 0
            for operation in operations:
                total_sum += operation.type*operation.value
            total_sum += account.initial_balance
            account_values[account] = total_sum
        context = super().get_context_data(**kwargs)
        context['accounts'] = accounts
        context['account_values'] = account_values
        return context


class AccountCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    
    model = Account
    fields = '__all__'
    template_name = 'account_create.html'

    def get_success_url(self):
        return reverse_lazy('account_list')


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Account
    fields = '__all__'
    template_name = 'account_create.html'

    def get_success_url(self):
        return reverse_lazy('account_list')


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    
    model = Account
    template_name = 'account_delete.html'

    def get_success_url(self):
        return reverse_lazy('account_list')


class AccountDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    
    model = Account
    template_name = 'account_detail.html'    

    def get_context_data(self, **kwargs):
        operations = Operation.objects.filter(account=self.object.pk)

        total_sum = 0
        for operation in operations:
            total_sum += operation.type*operation.value
        total_sum += self.object.initial_balance
        
        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        context['total_sum'] = total_sum
        return context


class DailyCostsView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    
    
    template_name = 'daily_costs.html'

    def __get_unique_dates(self):
        accounts = Account.objects.filter(user=self.request.user)
        operations = Operation.objects.filter(account__id__in=accounts.all())
        dates = []
        
        for operation in operations:
            if not (operation.date in dates):
                dates.append(operation.date)

        self.dates = dates

    def __process_date_operations(self):
        accounts = Account.objects.filter(user=self.request.user)
        dates_delta = {}
        for date in self.dates:
            accounts_delta = {}
            for account in accounts:
                daily_costs = 0
                operations = Operation.objects.filter(account=account,
                                                      date=date)
                for operation in operations:
                    daily_costs += operation.type*operation.value
                accounts_delta[account] = daily_costs
            dates_delta[date] = accounts_delta
        self.dates_delta = dates_delta
    
    def __get_daily_costs(self):
        daily_costs = {}
        for date in self.dates_delta:
            daily_cost = 0
            for account in self.dates_delta[date]:
                if account.calculated or account.type == 1:
                    daily_cost += self.dates_delta[date][account]

            daily_costs[date] = daily_cost
        self.daily_costs = daily_costs


    def get_context_data(self, **kwargs):
        self.__get_unique_dates()
        self.__process_date_operations()
        self.__get_daily_costs()

        context = super().get_context_data(**kwargs)
        context['delta'] = self.dates_delta
        context['cost'] = self.daily_costs
        return context
