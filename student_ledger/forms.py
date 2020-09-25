from django import forms
from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import AcademicSession, AcademicTerm, Bank, StudentClass, Student, StudentClass, Payment, Bill

class TermForm(ModelForm):
    class Meta:
        model = AcademicTerm
        fields = ['name','current']
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control form-control-sm", "placeholder": "Term Name"})
        }


class SessionForm(ModelForm):
    class Meta:
        model = AcademicSession
        fields = ['name', 'current']
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control form-control-sm", "placeholder": "Session Name. E.g 2012/2013"})
        }

class ClassForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
    class Meta:
        model = StudentClass
        fields = ['name', 'category']
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Class Name"})
        }

class BankForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Bank
        fields = ['name', 'code']
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Bank Name"}),
            "code": forms.TextInput(attrs={"placeholder": "Bank Code"})
        }


class StudentForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Student
        fields = '__all__'

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    session = forms.ModelChoiceField(AcademicSession.objects.all(), initial=0)
    term = forms.ModelChoiceField(AcademicTerm.objects.all(), initial=0)
    class_for = forms.ModelChoiceField(StudentClass.objects.all(), initial=0)



class BillForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Bill
        fields = '__all__'


class BillGenerateForm(BSModalForm):
    def __init__(self, *args, **kwargs):
        super(BillGenerateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    CLASSES = [
        ('primary', 'Primary'),
        ('junior', 'Junior'),
        ('secondary', 'Secondary'),
    ]
    session = forms.ModelChoiceField(
        AcademicSession.objects.all())
    term = forms.ModelChoiceField(
        AcademicTerm.objects.all())
    class_group = forms.ChoiceField(
        choices=CLASSES)

    def generate(self, formset):
        session = self.cleaned_data['session']
        term = self.cleaned_data['term']
        class_group = self.cleaned_data['class_group']
        students = Student.objects.filter(current_class__category=class_group)
        if students:
            for student in students:
                fm = copy.copy(formset)
                bill, created = Bill.objects.get_or_create(
                    student = student,
                    session=session,
                    term=term,
                    class_for=student.current_class,
                )
                if created:
                    fm.instance = bill
                    fm.save()


class BillPayForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Payment
        fields = ['bank', 'amount_paid', 'date', 'comment']
        widgets = {
            "date": forms.DateInput(attrs={"type":"date"}),
            "comment": forms.TextInput(),
        }
        labels = {
            "bill_item": "Bill Item (if related to an item)",
        }

class StatementSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    session = forms.ModelChoiceField(AcademicSession.objects.all(), initial=0)
    term = forms.ModelChoiceField(AcademicTerm.objects.all(), initial=0, required=False)
    class_for = forms.ModelChoiceField(StudentClass.objects.all(), initial=0, required=False)
