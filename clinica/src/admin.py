from django.contrib import admin
from .models import ClinicOwner, Secretary, Client, Dentist, UserStatus

# Register your models here.

admin.site.register(ClinicOwner)
admin.site.register(Secretary)
admin.site.register(Client)
admin.site.register(Dentist)
admin.site.register(UserStatus)  # Added