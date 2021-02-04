from django.forms import ModelForm,TextInput
import models
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['cityName']