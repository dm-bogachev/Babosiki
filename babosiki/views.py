from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic import *
from django.urls import reverse_lazy
from babosiki.forms import * 

class OperationTransferFormView(FormView):
    template_name = 'operation_transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('operation_list')

    def form_valid(self, form):
        form.transfer()
        return super().form_valid(form)
    

class OperationListView(TemplateView):
    template_name = "operation_list.html"

    def get_context_data(self, **kwargs):
        operations = Operation.objects.all()
        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        return context
    

class OperationDailyListView(TemplateView):
    
    template_name = "operation_daily_list.html"

    def get_context_data(self, **kwargs):
        date = self.kwargs.get('date', None)
        operations = Operation.objects.filter(date=date)

        delta = 0.0
        for operation in operations:
            delta += operation.value*operation.type


        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        context['delta'] = delta
        return context
    

class OperationCreateView(CreateView):
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


class OperationUpdateView(UpdateView):
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


class OperationDeleteView(DeleteView):
    model = Operation

    template_name = 'operation_delete.html'

    def __init__(self):
        super(OperationDeleteView, self).__init__()

    def get_success_url(self):
        return reverse_lazy('operation_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    template_name = 'category_create.html'

    def get_success_url(self):
        return reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'category_create.html'

    def get_success_url(self):
        return reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_delete.html'

    def get_success_url(self):
        return reverse_lazy('category_list')


class AccountListView(TemplateView):
    template_name = "account_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['operations'] = Operation.objects.all()
        return context


class AccountCreateView(CreateView):
    model = Account
    fields = '__all__'
    template_name = 'account_create.html'

    def get_success_url(self):
        return reverse_lazy('account_list')


class AccountUpdateView(UpdateView):
    model = Account
    fields = '__all__'
    template_name = 'account_create.html'

    def get_success_url(self):
        return reverse_lazy('account_list')


class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'account_delete.html'

    def get_success_url(self):
        return reverse_lazy('account_list')


class AccountDetailView(DetailView):
    model = Account
    template_name = 'account_detail.html'    


class DailyDeltaView(TemplateView):
    
    template_name = 'daily_costs.html'

    def __get_unique_dates(self):
        operations = Operation.objects.all()
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
