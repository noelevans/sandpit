from django import forms
from django.forms.models import ModelForm

from models import Venue


class VenueRegistrationForm(ModelForm):
    
    class Meta:
        model = Venue
        exclude = ('tags', 'contact')

