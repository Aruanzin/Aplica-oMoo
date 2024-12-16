from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from ..models import ClinicOwner, Secretary, Client, Dentist, UserStatus  # Updated import
from django.contrib.auth.models import User

class AuthController:
    @staticmethod
    def login_user(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = User.objects.get(username=username)
                status, created = UserStatus.objects.get_or_create(user=user)
                if status.is_locked:
                    messages.error(request, 'Sua conta está bloqueada. Por favor, verifique seu email para redefinir a senha.')
                    return False
            except User.DoesNotExist:
                user = None

            user = authenticate(request, username=username, password=password)
            if user is not None:
                status, created = UserStatus.objects.get_or_create(user=user)
                status.failed_attempts = 0
                status.save()
                login(request, user)
                return True
            else:
                if user:
                    status.failed_attempts += 1
                    if status.failed_attempts >= 3:
                        status.is_locked = True
                        status.save()
                        AuthController.send_lock_email(user)
                        messages.error(request, 'Sua conta foi bloqueada devido a múltiplas tentativas de login falhadas. Por favor, verifique seu email para redefinir a senha.')
                    else:
                        status.save()
                        messages.error(request, 'Usuário ou senha inválidos.')
                else:
                    messages.error(request, 'Usuário ou senha inválidos.')
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
            UserStatus.objects.create(user=user)  # Initialize UserStatus
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

    @staticmethod
    def send_lock_email(user):
        reset_link = f"{settings.FRONTEND_URL}/reset-password/?user={user.pk}"
        subject = 'Conta Bloqueada - Redefina sua Senha'
        message = f'Sua conta foi bloqueada devido a múltiplas tentativas de login falhadas. Por favor, redefina sua senha usando o link abaixo:\n\n{reset_link}'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
