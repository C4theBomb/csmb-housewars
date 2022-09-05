from django.forms import Form, ModelChoiceField, Select, ValidationError

from housewars.models import Activity


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

        # Verify that there are 60 minutes of activities selected
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
