from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, Dentist

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    ROLE_CHOICES = [
        ('clinic_owner', 'Dono da Clínica'),
        ('secretary', 'Secretária'),
        ('client', 'Cliente'),
        ('dentist', 'Dentista'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Tipo de usuário')
    specialization = forms.CharField(
        label='Especialização',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        specialization = cleaned_data.get('specialization')
        
        if role == 'dentist' and not specialization:
            raise forms.ValidationError('Especialização é obrigatória para dentistas.')
        
        return cleaned_data

class AppointmentRequestForm(forms.ModelForm):
    date = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    time = forms.ChoiceField(
        label='Horário',
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dentist = forms.ModelChoiceField(
        queryset=Dentist.objects.all(),
        label='Dentista',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['dentist', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        dentist = cleaned_data.get('dentist')
        date = cleaned_data.get('date')
        time_str = cleaned_data.get('time')

        if all([dentist, date, time_str]):
            time = datetime.strptime(time_str, '%H:%M').time()
            date_time = datetime.combine(date, time)
            cleaned_data['date_time'] = date_time

            # Verificar se o horário está disponível
            available_times = dentist.get_available_times(date)
            if date_time not in available_times:
                raise forms.ValidationError('Este horário não está mais disponível.')

        return cleaned_data
