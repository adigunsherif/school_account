from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView, BSModalFormView
from django.urls import reverse_lazy

from .models import Expense
from .forms import ExpenseForm


class ExpenseView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/list.html'


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
