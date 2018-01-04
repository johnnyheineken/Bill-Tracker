from django.forms import ModelForm
from polls.models import Person

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['name']
