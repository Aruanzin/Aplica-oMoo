from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterForm, AppointmentRequestForm
from .controllers.auth_controller import AuthController
from .controllers.appointment_controller import AppointmentController
from .models import Appointment, Dentist
from datetime import datetime

def login_view(request):
    if AuthController.login_user(request):
        return redirect('home')
    if request.method == 'POST':
        messages.error(request, 'Usuário ou senha inválidos.')
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

@login_required(login_url='login')
def home_view(request):
    user_type = None
    if hasattr(request.user, 'clinicowner'):
        user_type = 'clinic_owner'
    elif hasattr(request.user, 'secretary'):
        user_type = 'secretary'
    elif hasattr(request.user, 'dentist'):
        user_type = 'dentist'
    elif hasattr(request.user, 'client'):
        user_type = 'client'
    
    return render(request, 'accounts/home.html', {'user_type': user_type})

@login_required(login_url='login')
def request_appointment_view(request):
    if not hasattr(request.user, 'client'):
        messages.error(request, 'Apenas clientes podem solicitar consultas.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if AppointmentController.create_appointment(form, request.user.client):
            messages.success(request, 'Solicitação de consulta enviada.')
            return redirect('home')
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'accounts/request_appointment.html', {'form': form})

@login_required(login_url='login')
def get_available_times(request):
    dentist_id = request.GET.get('dentist_id')
    date_str = request.GET.get('date')
    
    try:
        dentist = Dentist.objects.get(id=dentist_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        available_times = dentist.get_available_times(date)
        
        times = [time.strftime('%H:%M') for time in available_times]
        return JsonResponse({'times': times})
    except (Dentist.DoesNotExist, ValueError):
        return JsonResponse({'times': []}, status=400)

@login_required(login_url='login')
def manage_appointments_view(request):
    if not hasattr(request.user, 'secretary'):
        messages.error(request, 'Apenas secretárias podem gerenciar consultas.')
        return redirect('home')
    appointments = AppointmentController.get_pending_appointments()
    return render(request, 'accounts/manage_appointments.html', {'appointments': appointments})

@login_required(login_url='login')
def accept_appointment_view(request, appointment_id):
    if not hasattr(request.user, 'secretary'):
        messages.error(request, 'Apenas secretárias podem aceitar consultas.')
        return redirect('home')
    appointment = get_object_or_404(Appointment, id=appointment_id, status='pending')
    appointment.status = 'accepted'
    appointment.secretary = request.user.secretary
    appointment.save()
    messages.success(request, 'Consulta aceita com sucesso.')
    return redirect('manage_appointments')

@login_required(login_url='login')
def reject_appointment_view(request, appointment_id):
    if not hasattr(request.user, 'secretary'):
        messages.error(request, 'Apenas secretárias podem recusar consultas.')
        return redirect('home')
    appointment = get_object_or_404(Appointment, id=appointment_id, status='pending')
    appointment.status = 'rejected'
    appointment.secretary = request.user.secretary
    appointment.save()
    messages.success(request, 'Consulta recusada com sucesso.')
    return redirect('manage_appointments')

@login_required(login_url='login')
def view_appointments(request):
    if hasattr(request.user, 'secretary') or hasattr(request.user, 'clinicowner'):
        appointments = AppointmentController.get_all_appointments()
    elif hasattr(request.user, 'dentist'):
        appointments = AppointmentController.get_dentist_appointments(request.user.dentist)
    else:
        messages.error(request, 'Acesso não autorizado.')
        return redirect('home')
    
    return render(request, 'accounts/view_appointments.html', {'appointments': appointments})