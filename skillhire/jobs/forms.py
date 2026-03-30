from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'required_skills']
        widgets = {
            'required_skills': forms.CheckboxSelectMultiple()
            }
        