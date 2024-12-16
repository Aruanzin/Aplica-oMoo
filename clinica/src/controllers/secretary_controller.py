from .validator import Validator
from ..models import Secretary, Appointment
from django.utils import timezone

class SecretaryController:
    @staticmethod
    def validate_secretary_data(data):
        if not Validator.validate_cpf(data.get('cpf')):
            return False, "CPF inválido"
        if not Validator.validate_phone(data.get('phone')):
            return False, "Telefone inválido"
        return True, "Dados válidos"

    @staticmethod
    def get_daily_appointments():
        today = timezone.now().date()
        return Appointment.objects.filter(date_time__date=today).order_by('date_time')

    @staticmethod
    def search_appointments(search_params):
        query = Appointment.objects.all()
        if 'client_name' in search_params:
            query = query.filter(client__user__username__icontains=search_params['client_name'])
        if 'date' in search_params:
            query = query.filter(date_time__date=search_params['date'])
        if 'status' in search_params:
            query = query.filter(status=search_params['status'])
        return query.order_by('date_time')
