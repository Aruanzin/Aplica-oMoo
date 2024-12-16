from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import ClinicOwner, Secretary, Client, Dentist

class AuthController:
    @staticmethod
    def login_user(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return True
            return False
        return None

    @staticmethod
    def logout_user(request):
        logout(request)

    @staticmethod
    def register_user(form):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            role = form.cleaned_data['role']
            
            if role == 'clinic_owner':
                ClinicOwner.objects.create(user=user)
            elif role == 'secretary':
                Secretary.objects.create(user=user)
            elif role == 'client':
                Client.objects.create(user=user)
            elif role == 'dentist':
                Dentist.objects.create(
                    user=user,
                    specialization=form.cleaned_data['specialization']
                )
            return True
        return False
