from django import forms
from .models import *

class ExploreForm(forms.ModelForm):
    class Meta:
        model=Destinations
        fields='__all__'

        Weather = forms.ChoiceField(
            choices=Destinations.CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'})
        )


