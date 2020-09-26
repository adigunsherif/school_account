from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView, BSModalFormView
from django.urls import reverse_lazy
from django.db.models.aggregates import Sum

from .models import Expense
from .forms import ExpenseForm, SearchForm


class ExpenseView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        params = {x:y for x, y in self.request.GET.items() if y}
        if params:
            queryset = queryset.filter(**params)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = SearchForm(initial=self.request.GET.dict())
        context['total'] = context['object_list'].aggregate(total=Sum('amount'))
        return context




class ExpenseCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')
    success_message = 'Expense added'
    template_name = 'expenses/create_form.html'
    context_object_name = 'object'


class ExpenseUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')
    success_message = 'Expense was successfully updated.'
    template_name = 'expenses/update_form.html'
    context_object_name = 'object'


class ExpenseDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Expense
    template_name = 'expenses/delete_form.html'
    success_message = 'Success: Expense was deleted.'
    success_url = reverse_lazy('expenses')
    context_object_name = "object"
