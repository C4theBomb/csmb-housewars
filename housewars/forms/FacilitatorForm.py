from django.forms import ModelForm, Select, TextInput

from housewars.models import Facilitator


class FacilitatorForm(ModelForm):
    class Meta:
        model = Facilitator
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'id': 'first-name',
                'placeholder': 'First Name'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'id': 'last-name',
                'placeholder': 'Last Name',
            }),
            'activity': Select(attrs={
                'class': 'form-select',
                'id': 'activity',
                'placeholder': 'activity'
            }),
        }
