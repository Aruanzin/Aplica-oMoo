
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string

def reset_password_view(request):
    user_id = request.GET.get('user')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuário inválido.')
        return redirect('login')

    if request.method == 'POST':
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            user.userstatus.failed_attempts = 0
            user.userstatus.is_locked = False
            user.userstatus.save()
            messages.success(request, 'Senha redefinida com sucesso. Você pode fazer login agora.')
            return redirect('login')
        else:
            messages.error(request, 'As senhas não coincidem.')

    return render(request, 'reset_password.html', {'user': user})