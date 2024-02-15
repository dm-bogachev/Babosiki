from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from babosiki.forms import * 

class TransferFormView(FormView):
    template_name = 'transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('operations')

    def form_valid(self, form):
        form.transfer()
        return super().form_valid(form)
    

class AccountListView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.all()
        context['operations'] = Operation.objects.all()
        return context


class OperationsListView(TemplateView):
    template_name = "operations.html"

    def get_context_data(self, **kwargs):
        operations = Operation.objects.all()
        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        return context
    
class DaysListView(TemplateView):
    template_name = "daily_costs.html"

    def get_context_data(self, **kwargs):
        operations = Operation.objects.all()

        Operation.objects.values_list('date', flat=True)

        days = {}

        for operation in operations:
            days[operation.date] = 0


        context = super().get_context_data(**kwargs)
        context['operations'] = operations
        #context['delta'] = delta
        return context
    

class DayListView(TemplateView):
    
    template_name = "operations_day.html"

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
    
class AddOperationView(CreateView):
    login_url = 'login'
    model = Operation
    fields = '__all__'
    exclude = ('user',)

    template_name = 'add_operation.html'

    def __init__(self):
        super(AddOperationView, self).__init__()

    def get_success_url(self):
        return reverse_lazy('operations')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddOperationView, self).form_valid(form)