from django import forms
from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):

    class Meta:
        model = CandidateProfile
        fields = '__all__'

        widgets = {

            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'education': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'experience': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'resume': forms.FileInput(attrs={
                'class': 'form-control' 
            }),

            'skills': forms.CheckboxSelectMultiple()
        }