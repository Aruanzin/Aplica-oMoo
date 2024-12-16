from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms.config_forms import SecretaryConfigForm, ClientConfigForm, DentistConfigForm, ClinicOwnerConfigForm

@login_required(login_url='login')
def configure_user_view(request):
    user = request.user
    if hasattr(user, 'secretary'):
        config = getattr(user, 'secretary')
        form = SecretaryConfigForm(instance=config)
    elif hasattr(user, 'client'):
        config = getattr(user, 'client')
        form = ClientConfigForm(instance=config)
    elif hasattr(user, 'dentist'):
        config = getattr(user, 'dentist')
        form = DentistConfigForm(instance=config)
    elif hasattr(user, 'clinicowner'):
        config = getattr(user, 'clinicowner')
        form = ClinicOwnerConfigForm(instance=config)
    else:
        messages.error(request, 'Tipo de usuário não reconhecido.')
        return redirect('home')

    if request.method == 'POST':
        if hasattr(user, 'secretary'):
            form = SecretaryConfigForm(request.POST, instance=config)
        elif hasattr(user, 'client'):
            form = ClientConfigForm(request.POST, instance=config)
        elif hasattr(user, 'dentist'):
            form = DentistConfigForm(request.POST, instance=config)
        elif hasattr(user, 'clinicowner'):
            form = ClinicOwnerConfigForm(request.POST, instance=config)

        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações atualizadas com sucesso.')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao atualizar configurações.')

    return render(request, 'configure_user.html', {'form': form})