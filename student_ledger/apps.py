from django.apps import AppConfig


class StudentLedgerConfig(AppConfig):
    name = 'student_ledger'

    def ready(self):
        import student_ledger.signals
