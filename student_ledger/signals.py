from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AcademicSession, AcademicTerm

@receiver(post_save, sender=AcademicSession)
def set_current_session(sender, instance, created, **kwargs):
    if  instance.current == True:
        sessions = AcademicSession.objects.exclude(id=instance.id).update(current=False)


@receiver(post_save, sender=AcademicTerm)
def set_current_for_term(sender, instance, created, **kwargs):
    if instance.current == True:
        academicterm = AcademicTerm.objects.exclude(id=instance.id).update(current=False)
