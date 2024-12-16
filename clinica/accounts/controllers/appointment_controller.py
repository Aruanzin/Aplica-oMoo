from ..models import Appointment

class AppointmentController:
    @staticmethod
    def create_appointment(form, client):
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = client
            appointment.save()
            return True
        return False

    @staticmethod
    def get_pending_appointments():
        return Appointment.objects.filter(status='pending')

    @staticmethod
    def get_all_appointments():
        return Appointment.objects.all().order_by('date_time')

    @staticmethod
    def get_dentist_appointments(dentist):
        return Appointment.objects.filter(dentist=dentist).order_by('date_time')

    @staticmethod
    def accept_appointment(appointment_id, secretary):
        try:
            appointment = Appointment.objects.get(id=appointment_id, status='pending')
            appointment.status = 'accepted'
            appointment.secretary = secretary
            appointment.save()
            return True
        except Appointment.DoesNotExist:
            return False

    @staticmethod
    def reject_appointment(appointment_id, secretary):
        try:
            appointment = Appointment.objects.get(id=appointment_id, status='pending')
            appointment.status = 'rejected'
            appointment.secretary = secretary
            appointment.save()
            return True
        except Appointment.DoesNotExist:
            return False
