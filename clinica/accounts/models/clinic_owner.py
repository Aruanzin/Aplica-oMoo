
from django.db import models
from django.contrib.auth.models import User

class ClinicOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birt_date = models.DateField(null=True)
    cpf = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.user.username