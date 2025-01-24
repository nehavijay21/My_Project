from django import forms
from .models import Programme, Department  # Ensure these models exist

class ProgramForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    level = forms.ChoiceField(
        choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate'), 
                 ('FYUG', 'Four Year UG'), ('IPG', 'Integrated PG')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Programme
        fields = ['programme_name', 'department', 'level', 'duration']
        widgets = {
            'programme_name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

