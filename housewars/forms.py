from django.forms import ModelForm, Form, CharField, EmailField, ChoiceField, ModelChoiceField, Select, TextInput, EmailInput, NumberInput, Textarea
from django.forms import ValidationError

from .models import Activity, House, PointsEntry, UserEntry


class UserEntryForm(Form):

    first_name = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'first-name',
        'placeholder': 'First Name'
    }))
    last_name = CharField(widget=TextInput(attrs={
        'class': "form-control",
        'id': 'last-name',
        'placeholder': 'Last Name'
    }))
    email = EmailField(widget=EmailInput(attrs={
        'class': "form-control",
        'id': 'email',
        'placeholder': 'Email'
    }))
    grade = ChoiceField(choices=UserEntry.GradeChoices, widget=Select(attrs={
        'class': "form-select",
        'id': 'grade',
        'placeholder': 'Grade'
    }))
    house = ModelChoiceField(House.objects.all(), widget=Select(attrs={
        'class': "form-select",
        'id': 'house',
        'placeholder': 'House'
    }))


class ActivityForm(Form):
    activity1 = ModelChoiceField(Activity.objects.all(), widget=Select(attrs={
        'class': "form-select",
        'id': 'activity1',
        'placeholder': 'Activity 1'
    }))
    activity2 = ModelChoiceField(Activity.objects.all(), required=False, widget=Select(attrs={
        'class': "form-select",
        'id': 'activity2',
        'placeholder': 'Activity 2'
    }))

    def clean(self):
        data = self.cleaned_data

        activity1 = data.get('activity1')
        activity2 = data.get('activity2')

        if activity1:
            if activity2 and activity1.time + activity2.time != 60:
                raise ValidationError(
                    "Please pick activities adding up to one hour.")
            elif not activity2 and activity1.time != 60:
                raise ValidationError(
                    "Please pick activities adding up to one hour.")
            else:
                super().clean()
        else:
            raise ValidationError("Please select an activity.")


class PointsEntryForm(ModelForm):
    class Meta:
        model = PointsEntry
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'id': 'first-name',
                'placeholder': 'Full Name'
            }),
            'activity': Select(attrs={
                'class': "form-select",
                'id': 'house',
                'placeholder': 'Activity'
            }),
            'house': Select(attrs={
                'class': "form-select",
                'id': 'house',
                'placeholder': 'House'
            }),
            'points': NumberInput(attrs={
                'class': "form-control",
                'id': 'last-name',
                'placeholder': 'Number of Points'
            }),
            'comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'first-name',
                'placeholder': 'Comments'
            })
        }
