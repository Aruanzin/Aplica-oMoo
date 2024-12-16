from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone

class ClinicOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.user.username

class DentalPlan(models.Model):
    type = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.type} - {self.number}"


class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)
    dental_plan = models.ForeignKey(DentalPlan, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

class Schedule(models.Model):
    WEEKDAYS = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    dentist = models.ForeignKey('Dentist', on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('dentist', 'weekday')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.start_time.strftime('%H:%M')} até {self.end_time.strftime('%H:%M')}"

class Dentist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)
    CRO = models.CharField(max_length=10, null=True)
    available_slots = models.IntegerField(default=30, help_text="Duração dos intervalos de consulta em minutos")
    
    def __str__(self):
        return self.user.username

    def get_available_times(self, date):
        weekday = date.weekday()
        schedule = self.schedules.filter(weekday=weekday, is_active=True).first()
        if not schedule:
            return []
        
        appointments = Appointment.objects.filter(
            dentist=self,
            date_time__date=date,
            status='accepted'
        ).values_list('date_time', flat=True)
        
        available_times = []
        current_time = datetime.combine(date, schedule.start_time)
        end_time = datetime.combine(date, schedule.end_time)
        
        while current_time < end_time:
            if current_time.time() >= timezone.now().time() or date > timezone.now().date():
                if current_time not in appointments:
                    available_times.append(current_time)
            current_time += timedelta(minutes=self.available_slots)
        
        return available_times

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('rejected', 'Recusado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    secretary = models.ForeignKey(Secretary, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dental_plan = models.ForeignKey(DentalPlan, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Consulta de {self.client.user.username} com Dr(a). {self.dentist.user.username} em {self.date_time}"

    class Meta:
        unique_together = ('dentist', 'date_time')