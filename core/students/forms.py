# In students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['created_at', 'success_probability']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'max': 22}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 4, 'step': 0.1}),
            'mother_education': forms.Select(attrs={'class': 'form-control'}),
            'father_education': forms.Select(attrs={'class': 'form-control'}),
            'travel_time': forms.Select(attrs={'class': 'form-control'}),
            'study_time': forms.Select(attrs={'class': 'form-control'}),
            'past_failures': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 4}),
            'family_relations': forms.Select(attrs={'class': 'form-control'}),
            'free_time': forms.Select(attrs={'class': 'form-control'}),
            'go_out': forms.Select(attrs={'class': 'form-control'}),
            'workday_alcohol': forms.Select(attrs={'class': 'form-control'}),
            'weekend_alcohol': forms.Select(attrs={'class': 'form-control'}),
            'health_status': forms.Select(attrs={'class': 'form-control'}),
            'absences': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 93}),
        }