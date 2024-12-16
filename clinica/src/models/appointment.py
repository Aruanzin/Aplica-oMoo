
from django.db import models
from .client import Client
from .dentist import Dentist
from .secretary import Secretary
from .dental_plan import DentalPlan

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