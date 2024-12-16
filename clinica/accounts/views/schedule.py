from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms.schedule_forms import ScheduleForm  # Atualizado
from ..models import Schedule

@login_required(login_url='login')
def manage_schedule_view(request):
    if not hasattr(request.user, 'dentist'):
        messages.error(request, 'Apenas dentistas podem gerenciar horários.')
        return redirect('home')
    
    dentist = request.user.dentist
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.dentist = dentist
            schedule.save()
            messages.success(request, 'Horário adicionado com sucesso.')
            return redirect('manage_schedule')
    else:
        form = ScheduleForm()
    
    schedules = Schedule.objects.filter(dentist=dentist)
    return render(request, 'accounts/manage_schedule.html', {
        'form': form,
        'schedules': schedules
    })

@login_required(login_url='login')
def toggle_schedule_view(request, schedule_id):
    if not hasattr(request.user, 'dentist'):
        messages.error(request, 'Operação não permitida.')
        return redirect('home')
    
    schedule = get_object_or_404(Schedule, id=schedule_id, dentist=request.user.dentist)
    schedule.is_active = not schedule.is_active
    schedule.save()
    
    status = 'ativado' if schedule.is_active else 'desativado'
    messages.success(request, f'Horário {status} com sucesso.')
    return redirect('manage_schedule')