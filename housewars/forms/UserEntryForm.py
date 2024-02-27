from django.forms import (CharField, ChoiceField, EmailField, EmailInput,
                          Form, ModelChoiceField, Select, TextInput, ValidationError)

from housewars.models import House, UserEntry


class UserEntryForm(Form):
    first_name = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'first-name',
        'placeholder': 'First'
    }))
    last_name = CharField(widget=TextInput(attrs={
        'class': "form-control",
        'id': 'last-name',
        'placeholder': 'Last'
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

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Verify that email domain matches
        if ('@slps.org' not in email):
            raise ValidationError("Please use your school email.")
        # Verify that the email is unique
        if UserEntry.objects.filter(email=email).exists():
            raise ValidationError(
                "A signup with this email already exists, if you want to change your signups, please email ipatino3341@slps.org.")

        return email
