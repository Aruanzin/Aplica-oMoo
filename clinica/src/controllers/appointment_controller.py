from ..models import Appointment
from django.utils import timezone
from datetime import datetime
from ..settings import USE_TZ

class AppointmentController:
    @staticmethod
    def create_appointment(form, client):
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = client
            
            # Get date and time from form
            date = form.cleaned_data.get('date')
            time_str = form.cleaned_data.get('time')
            
            # Create datetime object
            try:
                time = datetime.strptime(time_str, '%H:%M').time()
                date_time = datetime.combine(date, time)
                if USE_TZ:
                    date_time = timezone.make_aware(date_time)
                
                appointment.date_time = date_time
                appointment.save()
                return True
            except (ValueError, TypeError) as e:
                print(f"Error creating appointment: {e}")
                return False
        return False

    @staticmethod
    def get_pending_appointments():
        return Appointment.objects.filter(status='pending')

    @staticmethod
    def get_all_appointments():
        return Appointment.objects.all().order_by('date_time')

    @staticmethod
    def get_dentist_appointments(dentist):
        return Appointment.objects.filter(
            dentist=dentist,
            status='accepted'
        ).order_by('date_time')

    @staticmethod
    def get_client_appointments(client):
        return Appointment.objects.filter(
            client=client
        ).order_by('date_time')

    @staticmethod
    def get_accepted_appointments():
        return Appointment.objects.filter(
            status='accepted'
        ).order_by('date_time')

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
