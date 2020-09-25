from django.conf import settings
from django.utils.html import mark_safe
from .models import AcademicSession, AcademicTerm


def default(request):
    try:
        session = AcademicSession.objects.get(current=True)
    except AcademicSession.DoesNotExist:
        session = ''

    try:
        term = AcademicTerm.objects.get(current=True)
    except AcademicTerm.DoesNotExist:
        term = ''

    data = {
        "app_name": settings.APP_NAME,
        "current_session": session,
        "current_term": term,
        "currency": mark_safe(settings.CURRENCY),
    }
    return data
