from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

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
