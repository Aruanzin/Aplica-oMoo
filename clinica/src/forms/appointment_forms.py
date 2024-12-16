
from django import forms
from ..controllers import DentistController
from ..models import Appointment
from datetime import datetime
from django.utils import timezone
from ..settings import USE_TZ

class AppointmentRequestForm(forms.ModelForm):
    date = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    time = forms.CharField(
        label='Horário',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dentist = forms.ModelChoiceField(
        queryset=DentistController.get_active_dentists(),
        label='Dentista',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['dentist']  # Remove date_time from here

    def clean(self):
        cleaned_data = super().clean()
        dentist = cleaned_data.get('dentist')
        date = cleaned_data.get('date')
        time_str = cleaned_data.get('time')

        if all([dentist, date, time_str]):
            try:
                # Convert time string to time object
                time_obj = datetime.strptime(time_str, '%H:%M').time()
                # Combine date and time
                date_time = datetime.combine(date, time_obj)
                
                # Make timezone-aware if using timezones
                if USE_TZ:
                    date_time = timezone.make_aware(date_time)
                
                # Store both the original fields and the combined date_time
                cleaned_data['date_time'] = date_time
                
                # Verify availability
                available_times = dentist.get_available_times(date)
                if not any(t.strftime('%H:%M') == time_str for t in available_times):
                    raise forms.ValidationError('Este horário não está mais disponível.')
                
            except ValueError as e:
                raise forms.ValidationError(f'Erro ao processar a data/hora: {str(e)}')
        else:
            raise forms.ValidationError('Todos os campos são obrigatórios.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget.choices = []