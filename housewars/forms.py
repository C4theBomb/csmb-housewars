from django.forms import ModelForm, TextInput, EmailInput
from django.db.models import F

from .models import Entry, Activity


class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = '__all__'

    widgets = {
        'first_name': TextInput(attrs={
            'class': "form-control",
            'style': 'max-width: 1px;',
            'placeholder': 'Name'
        }),
        'last_name': TextInput(attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'Last Name'
        }),
        'email': EmailInput(attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'Email'
        }),
        'grade': TextInput(attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'Grade'
        }),
        'house': TextInput(attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'House'
        }),
        'activity1': TextInput(attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'Activity 1'
        }),
        'activity2': TextInput(attrs={
            'class': "form-control",
            'style': 'max-width: 300px;',
            'placeholder': 'Activity 2'
        }),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filtered1 = Activity.session1.below_quota()
        filtered2 = Activity.session2.below_quota()

        self.fields['activity1'].queryset = filtered1
        self.fields['activity2'].queryset = filtered2
