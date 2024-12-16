from .validator import Validator
from ..models import Dentist, Appointment, Schedule
from django.utils import timezone

class DentistController:
    @staticmethod
    def validate_dentist_data(data):
        if not Validator.validate_cpf(data.get('cpf')):
            return False, "CPF inválido"
        if not Validator.validate_phone(data.get('phone')):
            return False, "Telefone inválido"
        if not Validator.validate_cro(data.get('cro')):
            return False, "CRO inválido"
        return True, "Dados válidos"

    @staticmethod
    def get_dentist_schedule(dentist_id, date):
        try:
            dentist = Dentist.objects.get(id=dentist_id)
            appointments = Appointment.objects.filter(
                dentist=dentist,
                date_time__date=date,
                status='accepted'
            ).order_by('date_time')
            return appointments
        except Dentist.DoesNotExist:
            return None

    @staticmethod
    def check_availability(dentist_id, date_time):
        try:
            dentist = Dentist.objects.get(id=dentist_id)
            existing_appointment = Appointment.objects.filter(
                dentist=dentist,
                date_time=date_time,
                status='accepted'
            ).exists()
            return not existing_appointment
        except Dentist.DoesNotExist:
            return False

    @staticmethod
    def add_schedule(dentist_id, weekday, start_time, end_time):
        try:
            dentist = Dentist.objects.get(id=dentist_id)
            schedule = Schedule.objects.create(
                dentist=dentist,
                weekday=weekday,
                start_time=start_time,
                end_time=end_time
            )
            return True, schedule
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_dentist_schedules(dentist_id):
        try:
            dentist = Dentist.objects.get(id=dentist_id)
            return Schedule.objects.filter(dentist=dentist)
        except Dentist.DoesNotExist:
            return None

    @staticmethod
    def update_schedule(schedule_id, start_time=None, end_time=None, is_active=None):
        try:
            schedule = Schedule.objects.get(id=schedule_id)
            if start_time:
                schedule.start_time = start_time
            if end_time:
                schedule.end_time = end_time
            if is_active is not None:
                schedule.is_active = is_active
            schedule.save()
            return True
        except Schedule.DoesNotExist:
            return False
