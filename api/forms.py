from django import forms
from .models import City
import re

class WeatherQueryForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city']
        labels = {'city': ''}
        widgets = {
            'city': forms.TextInput(
                attrs={
                'id': 'city-input',
                'placeholder': 'Enter at least 3 letters to see suggestions',
                'class': 'form-control',
                'required': True
                }
            ),
        }

    def clean_city(self):
        city = self.cleaned_data['city'].strip()
        
        if not re.match(r'^[^\d\W_]+(?:[\s-][^\d\W_]+)*$', city, re.UNICODE):
            raise forms.ValidationError("City name should contain only letters, spaces, or hyphens.")
        return city

