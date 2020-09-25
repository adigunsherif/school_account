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



# Create your views here.

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

class BillListView(LoginRequiredMixin, ListView):
    model = Bill

    def get_queryset(self):
        queryset = Bill.objects.none()
        req = self.request.GET
        params = req.dict()
        if params:
            queryset = Bill.objects.filter(**params)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payable = 0
        paid = 0
        balance = 0
        credit = 0

        for bill in context['object_list']:
            payable += bill.total
            paid += bill.paid
            balance += bill.balance
            credit += bill.credit

        totals = [payable, paid, balance, credit]
        context['totals'] = totals
        req = self.request.GET
        params = dict(req.dict())
        context['search'] = SearchForm(initial=params)
        return context


class BillCreateView(LoginRequiredMixin, BSModalCreateView):
    form_class = BillForm
    success_url = reverse_lazy('bills')
    template_name = 'student_ledger/create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add a new bill'
        context['button'] = 'Create invoice'
        return context


class BillGenerateView(LoginRequiredMixin, BSModalFormView):
    form_class = BillGenerateForm
    template_name = 'student_ledger/generate-bill.html'
    success_url = reverse_lazy('bills')
    success_message = "Bills successfully created"



    def form_valid(self, form):
        if not self.request.is_ajax():
            context = self.get_context_data()
            formset = context['bill_item']
            form.generate(formset)
        return super().form_valid(form)


class BillPay(BSModalCreateView):
    form_class = BillPayForm
    template_name = 'student_ledger/create_form.html'
    success_url = reverse_lazy('bills')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BillPay, self).get_form_kwargs(*args, **kwargs)
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal_credit'] = Journal.objects.filter(bill=self.object, journal_type='credit')
        context['journal_debit'] = Journal.objects.filter(bill=self.object, journal_type='debit')
        return context



class StatementView(LoginRequiredMixin, View):
    """ Show statement for student bills """

    template_name = 'student_ledger/statement.html'
    form_class = StatementSearchForm

    def get(self, request, *args, **kwargs):
        params = {x:y for x, y in request.GET.items() if y}
        context = {
            "search": self.form_class(initial=params),
        }
        if params:
            bills = Bill.objects.filter(**params)

            total_bill = 0
            total_paid = 0
            total_debt = 0
            total_credit = 0
            for bill in bills:
                total_bill += bill.total
                total_paid += bill.paid
                total_debt += bill.balance
                total_credit += bill.credit

            bill_total = (total_bill, total_paid, total_debt, total_credit)

            #Bill items
            bill_items = BillItem.objects.filter(bill__in=bills)

            #payments
            payments = Payment.objects.filter(bill__in=bills)

            categories = {}

            bill_item_total = 0

            for cat in bill_items.values('bill_category', 'bill_category__name').distinct():
                for item in bill_items.filter(bill_category_id=cat['bill_category']):
                    bill_item_total += item.total

                p = payments.filter(bill_item__bill_category=cat['bill_category']).aggregate(Sum('amount_paid'))

                categories[cat['bill_category__name']] = [bill_item_total, p['amount_paid__sum']]

            #banks
            banks = {}
            for bank in payments.values('bank', 'bank__name').distinct():
                b = payments.filter(bank_id=bank['bank']).aggregate(Sum('amount_paid'))
                banks[bank['bank__name']] = b['amount_paid__sum']

            context["bills"] = bills
            context["bill_totals"] = bill_total
            context["categories"] = categories
            context["banks"] = banks
            #context["d"]


        return render(request, self.template_name, context)
