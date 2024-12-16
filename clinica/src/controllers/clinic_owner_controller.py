from sympy import Sum
from .validator import Validator
from ..models import ClinicOwner, Appointment, Dentist
from django.db.models import Count
from django.utils import timezone

class ClinicOwnerController:
    @staticmethod
    def validate_owner_data(data):
        if not Validator.validate_cpf(data.get('cpf')):
            return False, "CPF inválido"
        if not Validator.validate_phone(data.get('phone')):
            return False, "Telefone inválido"
        return True, "Dados válidos"

    @staticmethod
    def get_clinic_statistics():
        today = timezone.now().date()
        stats = {
            'total_appointments': Appointment.objects.count(),
            'today_appointments': Appointment.objects.filter(date_time__date=today).count(),
            'dentists_count': Dentist.objects.count(),
            'appointments_by_dentist': Appointment.objects.values('dentist__user__username')
                                              .annotate(total=Count('id'))
        }
        return stats

    @staticmethod
    def get_monthly_report(year, month):
        appointments = Appointment.objects.filter(
            date_time__year=year,
            date_time__month=month
        )
        report = {
            'total_appointments': appointments.count(),
            'accepted_appointments': appointments.filter(status='accepted').count(),
            'rejected_appointments': appointments.filter(status='rejected').count(),
            'revenue': appointments.filter(status='accepted').aggregate(Sum('value'))['value__sum'] or 0
        }
        return report
