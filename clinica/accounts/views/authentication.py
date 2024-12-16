from django.shortcuts import render, redirect
from django.contrib import messages
from ..controllers.auth_controller import AuthController
from ..forms.auth_forms import RegisterForm  # Atualizado

def login_view(request):
    if AuthController.login_user(request):
        return redirect('home')
    return render(request, 'accounts/login.html')

def logout_view(request):
    AuthController.logout_user(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if AuthController.register_user(form):
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})