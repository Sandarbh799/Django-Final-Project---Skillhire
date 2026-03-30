from django import forms
from .models import Interview
from datetime import datetime


class InterviewForm(forms.ModelForm):

    AM_PM_CHOICES = (
        ('AM', 'AM'),
        ('PM', 'PM'),
    )

    am_pm = forms.ChoiceField(choices=AM_PM_CHOICES)    
       
    class Meta:

        model = Interview
        fields = ['date', 'time', 'mode', 'meeting_link', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(
                format='%I:%M %p',
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')

        if selected_date and selected_time:
            now = datetime.now()

            # Combine date + time
            selected_datetime = datetime.combine(selected_date, selected_time)

            if selected_datetime < now:
                raise forms.ValidationError("Past date/time not allowed!")

        return cleaned_data