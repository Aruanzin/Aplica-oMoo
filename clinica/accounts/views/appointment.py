from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms.appointment_forms import AppointmentRequestForm  # Atualizado
from ..controllers.appointment_controller import AppointmentController
from ..models import Appointment, Dentist
from datetime import datetime


@login_required(login_url='login')
def request_appointment_view(request):
    if not hasattr(request.user, 'client'):
        messages.error(request, 'Apenas clientes podem solicitar consultas.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            try:
                if AppointmentController.create_appointment(form, request.user.client):
                    messages.success(request, 'Solicitação de consulta enviada.')
                    return redirect('home')
                else:
                    messages.error(request, 'Erro ao criar a consulta.')
            except Exception as e:
                messages.error(request, f'Erro ao processar a solicitação: {str(e)}')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'accounts/request_appointment.html', {'form': form})

@login_required(login_url='login')
def get_available_times(request):
    dentist_id = request.GET.get('dentist_id')
    date_str = request.GET.get('date')
    
    print(f"Received request for dentist_id: {dentist_id}, date: {date_str}")
    
    try:
        dentist = Dentist.objects.get(id=dentist_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        schedule = dentist.schedules.filter(weekday=date.weekday(), is_active=True).first()
        if not schedule:
            print(f"No schedule found for weekday: {date.weekday()}")
            return JsonResponse({'times': [], 'message': 'Não há horários disponíveis para este dia'})
            
        available_times = dentist.get_available_times(date)
        times = [time.strftime('%H:%M') for time in available_times]
        
        print(f"Available times being sent: {times}")
        return JsonResponse({
            'times': times,
            'debug_info': {
                'weekday': date.weekday(),
                'schedule_exists': bool(schedule),
                'available_times_count': len(times)
            }
        })
    except (Dentist.DoesNotExist, ValueError) as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'times': [], 'error': str(e)}, status=400)

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
    if hasattr(request.user, 'secretary'):
        # Secretárias veem todas as consultas
        appointments = AppointmentController.get_all_appointments()
    elif hasattr(request.user, 'clinicowner'):
        # Donos da clínica veem apenas consultas aceitas
        appointments = AppointmentController.get_accepted_appointments()
    elif hasattr(request.user, 'dentist'):
        # Dentistas veem apenas suas consultas aceitas
        appointments = AppointmentController.get_dentist_appointments(request.user.dentist)
    elif hasattr(request.user, 'client'):
        # Clientes veem suas próprias consultas (todas)
        appointments = AppointmentController.get_client_appointments(request.user.client)
    else:
        messages.error(request, 'Acesso não autorizado.')
        return redirect('home')
    
    return render(request, 'accounts/view_appointments.html', {'appointments': appointments})