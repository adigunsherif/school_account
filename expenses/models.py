from django.db import models
from django.utils.timezone import now

from student_ledger.models import AcademicTerm, AcademicSession

class Expense(models.Model):
    short_description = models.CharField(max_length=200)
    date = models.DateField(default=now)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True)
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    additional_comment = models.TextField()

    def __str__(self):
        return f'{self.short_description}'
