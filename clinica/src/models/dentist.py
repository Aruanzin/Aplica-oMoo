
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

class Dentist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)
    CRO = models.CharField(max_length=10, null=True)
    available_slots = models.IntegerField(default=30, help_text="Duração dos intervalos de consulta em minutos")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username

    def get_available_times(self, date):
        from .appointment import Appointment
        
        weekday = date.weekday()
        schedule = self.schedules.filter(weekday=weekday, is_active=True).first()
        
        # Debug print
        print(f"Schedule found: {schedule}")
        
        if not schedule:
            return []
        
        appointments = Appointment.objects.filter(
            dentist=self,
            date_time__date=date,
            status='accepted'
        ).values_list('date_time', flat=True)
        
        available_times = []
        current_time = datetime.combine(date, schedule.start_time)
        current_time = timezone.make_aware(current_time)  # Torna o datetime aware
        
        end_time = datetime.combine(date, schedule.end_time)
        end_time = timezone.make_aware(end_time)  # Torna o datetime aware
        
        now = timezone.now()
        
        while current_time < end_time:
            # Se a data for hoje, só mostra horários futuros
            if date == now.date():
                if current_time > now:
                    if current_time not in appointments:
                        available_times.append(current_time)
            else:
                # Se for data futura, mostra todos os horários
                if current_time not in appointments:
                    available_times.append(current_time)
            
            current_time += timedelta(minutes=self.available_slots)
        
        # Debug print
        print(f"Available times: {available_times}")
        
        return available_times