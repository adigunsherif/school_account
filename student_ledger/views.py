from django.db.models.functions import Coalesce
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models.aggregates import Sum
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView, BSModalFormView

from .models import Student, StudentClass, Bank, Bill, Payment, AcademicSession, AcademicTerm

from .forms import StudentForm, TermForm, SessionForm, ClassForm, BankForm, BillForm, BillGenerateForm, BillPayForm, StatementSearchForm, SearchForm


@login_required
def settings_view(request):
    if request.method == 'POST':
        termform = TermForm(request.POST, prefix='term')
        if termform.is_valid():
            termform.save()

        sessionform = SessionForm(request.POST, prefix='session')
        if sessionform.is_valid():
            sessionform.save()

        classform = ClassForm(request.POST, prefix='classes')
        if classform.is_valid():
            classform.save()

        bankform = BankForm(request.POST, prefix='banks')
        if bankform.is_valid():
            bankform.save()



    terms = AcademicTerm.objects.all()
    sessions = AcademicSession.objects.all()
    classes = StudentClass.objects.all()
    banks = Bank.objects.all()

    termform = TermForm(prefix='term')
    sessionform = SessionForm(prefix='session')
    classform = ClassForm(prefix='classes')
    bankform = BankForm(prefix="banks")

    context = {
        "terms": terms,
        "sessions":sessions,
        "classes": classes,
        "banks": banks,
        "term_form": termform,
        "session_form": sessionform,
        "class_form": classform,
        "bank_form": bankform,
    }

    return render(request, 'student_ledger/settings.html', context)


class SessionUpdateForm(LoginRequiredMixin, BSModalUpdateView):
    model = AcademicSession
    form_class = SessionForm
    template_name = 'student_ledger/update_form.html'
    success_url = reverse_lazy('settings')
    context_object_name = 'object'


class TermUpdateForm(LoginRequiredMixin, BSModalUpdateView):
    model = AcademicTerm
    form_class = TermForm
    template_name = 'student_ledger/update_form.html'
    success_url = reverse_lazy('settings')
    context_object_name = 'object'


class ClassUpdateForm(LoginRequiredMixin, BSModalUpdateView):
    model = StudentClass
    form_class = ClassForm
    template_name = 'student_ledger/update_form.html'
    success_url = reverse_lazy('settings')
    context_object_name = 'object'


class BankUpdateForm(LoginRequiredMixin, BSModalUpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'student_ledger/update_form.html'
    success_url = reverse_lazy('settings')
    context_object_name = 'object'


class StudentListView(LoginRequiredMixin, ListView):
    model = Student


class StudentCreateView(LoginRequiredMixin, BSModalCreateView):
    form_class = StudentForm
    success_url = reverse_lazy('students')
    success_message = 'Student was successfully created.'
    template_name = 'student_ledger/create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register new student'
        context['button'] = 'Save new student'
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student_ledger/student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register new student'
        context['button'] = 'Save new student'
        return context


class StudentUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('students')
    success_message = 'Student was successfully updated.'
    template_name = 'student_ledger/update_form.html'
    context_object_name = 'object'


class StudentDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Student
    template_name = 'student_ledger/delete_form.html'
    success_message = 'Success: Student was deleted.'
    success_url = reverse_lazy('students')
    context_object_name = "object"


"""

   **********************  BILLS  ****************

"""

class BillListView(LoginRequiredMixin, View):
    """ Show statement for student bills """
    template_name = 'student_ledger/statement.html'
    form_class = StatementSearchForm

    def get(self, request, *args, **kwargs):
        params = {x:y for x, y in request.GET.items() if y}
        aggregation = {
            "total_bill": Coalesce(Sum('amount_payable'),0),
            "total_paid": Coalesce(Sum('payment__amount_paid'), 0),
            "total_debt": Coalesce(Sum('amount_payable'), 0) - Coalesce(Sum('payment__amount_paid'), 0)
        }

        bills = Bill.objects.all()
        bills_aggregate = bills.aggregate(**aggregation)

        if params:
            bills = Bill.objects.filter(**params)
            bills_aggregate = bills.aggregate(**aggregation)

        context = {
            "search": self.form_class(initial=params),
            "bills": bills,
            "bills_aggregate":bills_aggregate,
        }
        return render(request, self.template_name, context)


class BillCreateView(LoginRequiredMixin, BSModalCreateView):
    form_class = BillForm
    success_url = reverse_lazy('home')
    template_name = 'student_ledger/create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add a new bill'
        context['button'] = 'Create invoice'
        return context


class BillGenerateView(LoginRequiredMixin, BSModalFormView):
    form_class = BillGenerateForm
    template_name = 'student_ledger/generate-bill.html'
    success_url = reverse_lazy('home')
    success_message = "Bills successfully created"


    def form_valid(self, form):
        if not self.request.is_ajax():
            class_for = form.cleaned_data['class_for']
            session = form.cleaned_data['session']
            term = form.cleaned_data['term']
            amount_payable = form.cleaned_data['amount_payable']
            students = Student.objects.filter(current_class=class_for, active=True)
            bills = []
            for student in students:
                bills.append(Bill(
                    student=student,
                    session=session,
                    term=term,
                    class_for=class_for,
                    amount_payable=amount_payable
                ))
            Bill.objects.bulk_create(bills)

        return super().form_valid(form)


class BillPay(BSModalCreateView):
    form_class = BillPayForm
    template_name = 'student_ledger/create_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Payment'
        context['button'] = 'Add payment'
        return context

    def form_valid(self, form):
        bill = get_object_or_404(Bill, pk=self.kwargs['pk'])
        form.instance.bill = bill
        return super().form_valid(form)


class BillDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = "student_ledger/bill-detail.html"



class BillUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Bill
    form_class = BillForm
    success_url = reverse_lazy('home')
    success_message = 'Bill was successfully updated.'
    template_name = 'student_ledger/update_form.html'
    context_object_name = 'object'


class BillDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Bill
    template_name = 'student_ledger/delete_form.html'
    success_message = 'Success: Bill was deleted.'
    success_url = reverse_lazy('home')
    context_object_name = "object"


class PaymentDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Payment
    template_name = 'student_ledger/delete_form.html'
    success_message = 'Success: Payment was deleted.'
    context_object_name = "object"

    def get_success_url(self):
        return self.object.bill.get_absolute_url()

