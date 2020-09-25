from django.db import models

class StudentClass(models.Model):
    CATEGORIES = [
        ('primary', 'Primary'),
        ('junior', 'Junior'),
        ('secondary', 'Secondary'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} ({self.code})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'code'], name='unique_bank'),
        ]


class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_names = models.CharField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=200, blank=True)
    current_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.surname} {self.firstname} {self.other_names}'


class Bill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    class_for = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True)
    amount_payable = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.student}'s bill"

    @property
    def paid(self):
        tt = Payment.objects.filter(bill=self).aggregate(Sum('amount_paid'))
        val = tt['amount_paid__sum'] if tt['amount_paid__sum'] else 0
        return val

    @property
    def balance(self):
        total = self.total - self.paid
        return 0 if total < 0 else total

    @property
    def credit(self):
        total = self.total - self.paid
        if total > 0:
            return  0
        else: return abs(total)


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField()
    comment = models.TextField(blank=True)
