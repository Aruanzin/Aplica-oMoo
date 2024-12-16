
from django import forms
from ..models import Secretary, Client, Dentist, ClinicOwner

class SecretaryConfigForm(forms.ModelForm):
    class Meta:
        model = Secretary
        fields = ['birt_date', 'cpf', 'phone']
        widgets = {
            'birt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'birt_date': 'Data de Nascimento',
            'cpf': 'CPF',
            'phone': 'Telefone',
        }

class ClientConfigForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['birt_date', 'cpf', 'phone', 'dental_plan']
        widgets = {
            'birt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'dental_plan': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'birt_date': 'Data de Nascimento',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'dental_plan': 'Plano Odontológico',
        }

class DentistConfigForm(forms.ModelForm):
    class Meta:
        model = Dentist
        fields = ['specialization', 'birt_date', 'cpf', 'phone', 'CRO', 'available_slots', 'is_active']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'birt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'CRO': forms.TextInput(attrs={'class': 'form-control'}),
            'available_slots': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'specialization': 'Especialização',
            'birt_date': 'Data de Nascimento',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'CRO': 'CRO',
            'available_slots': 'Vagas Disponíveis',
            'is_active': 'Ativo',
        }

class ClinicOwnerConfigForm(forms.ModelForm):
    class Meta:
        model = ClinicOwner
        fields = ['birt_date', 'cpf', 'phone']
        widgets = {
            'birt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'birt_date': 'Data de Nascimento',
            'cpf': 'CPF',
            'phone': 'Telefone',
        }