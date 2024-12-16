
from django.db import models
from django.contrib.auth.models import User
from .dental_plan import DentalPlan

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)
    dental_plan = models.ForeignKey(DentalPlan, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username