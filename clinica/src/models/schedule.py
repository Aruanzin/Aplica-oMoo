
from django.db import models
from .dentist import Dentist

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

    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('dentist', 'weekday')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.start_time.strftime('%H:%M')} até {self.end_time.strftime('%H:%M')}"