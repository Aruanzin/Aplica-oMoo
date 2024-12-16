from .validator import Validator
from ..models import Client, Appointment

class ClientController:
    @staticmethod
    def validate_client_data(data):
        if not Validator.validate_cpf(data.get('cpf')):
            return False, "CPF inválido"
        if not Validator.validate_phone(data.get('phone')):
            return False, "Telefone inválido"
        return True, "Dados válidos"

    @staticmethod
    def get_client_appointments(client_id):
        try:
            client = Client.objects.get(id=client_id)
            return Appointment.objects.filter(client=client).order_by('-date_time')
        except Client.DoesNotExist:
            return None

    @staticmethod
    def update_dental_plan(client_id, dental_plan_id):
        try:
            client = Client.objects.get(id=client_id)
            client.dental_plan_id = dental_plan_id
            client.save()
            return True
        except Client.DoesNotExist:
            return False
