
from django.db import models

class DentalPlan(models.Model):
    type = models.CharField(max_length=50)
    number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type} - {self.number}"