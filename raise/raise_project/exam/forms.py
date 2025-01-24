from django import forms
from .models import Programme  # Assuming Program is your model name

class ProgramForm(forms.ModelForm):
    LEVEL_CHOICES = [
        ('U', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('FYUG', 'Four Year Undergraduate'),
        ('IPG', 'Integrated Postgraduate'),
    ]

    level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Programme
        fields = ['programme_name', 'dept', 'level', 'duration']
        widgets = {
            'programme_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
