from django.forms import ModelForm, TextInput, EmailInput, Select
from django.db.models import F

from .models import Entry, Activity


class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = '__all__'

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'id': 'first-name',
                'placeholder': 'First Name'
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'id': 'last-name',
                'placeholder': 'Last Name'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'id': 'email',
                'placeholder': 'Email'
            }),
            'grade': Select(attrs={
                'class': "form-select",
                'id': 'grade',
                'placeholder': 'Grade'
            }),
            'house': Select(attrs={
                'class': "form-select",
                'id': 'house',
                'placeholder': 'House'
            }),
            'activity1': Select(attrs={
                'class': "form-select",
                'id': 'activity1',
                'placeholder': 'Activity 1'
            }),
            'activity2': Select(attrs={
                'class': "form-select",
                'id': 'activity2',
                'placeholder': 'Activity 2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filtered1 = Activity.session1.below_quota()
        filtered2 = Activity.session2.below_quota()

        self.fields['activity1'].queryset = filtered1
        self.fields['activity2'].queryset = filtered2
