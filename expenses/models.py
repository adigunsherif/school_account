from django.db import models
from django.utils.timezone import now

class Expense(models.Model):
    short_description = models.CharField(max_length=200)
    date = models.DateField(default=now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    additional_comment = models.TextField()


    def __str__(self):
        return f'{self.short_description}'
