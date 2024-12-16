from django import forms
from django.contrib.auth.models import User

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

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'Por favor, insira um endereço de email válido.',
        }
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
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        role = cleaned_data.get('role')
        specialization = cleaned_data.get('specialization')

        # Verificar se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Este nome de usuário já está em uso.')

        # Verificar se o email já existe
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Este email já está em uso.')

        # Verificar se a especialização foi fornecida para dentistas
        if role == 'dentist' and not specialization:
            self.add_error('specialization', 'Especialização é obrigatória para dentistas.')

        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email