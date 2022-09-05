from django.forms import ModelForm, Select, TextInput
from housewars.models import Activity, House, PointsEntry, UserEntry


class PointsEntryForm(ModelForm):
    class Meta:
        model = PointsEntry
        fields = '__all__'
        widgets = {
            'house': Select(attrs={
                'class': "form-select",
                'id': 'house',
                'placeholder': 'House'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'id': 'first-name',
                'placeholder': 'Password',
                'type': 'password'
            })
        }

    def __init__(self, *args, **kwargs):
        super(PointsEntryForm, self).__init__(*args, **kwargs)
        self.fields['activity'].widget.attrs.update({'class': 'form-select'})
        self.fields['award'].widget.attrs.update({'class': 'form-select'})
