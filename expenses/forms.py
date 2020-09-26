from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from student_ledger.models import AcademicTerm, AcademicSession
from .models import Expense

class ExpenseForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Expense
        exclude = ()
        widgets = {
            "date": forms.DateInput(attrs={"type":"date"}),
        }


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    session = forms.ModelChoiceField(AcademicSession.objects.all(), initial=0)
    term = forms.ModelChoiceField(AcademicTerm.objects.all(), initial=0, required=False)
