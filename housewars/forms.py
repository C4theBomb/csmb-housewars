from django.forms import ModelForm
from django.db.models import F

from .models import Entry, Activity


class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filtered1 = Activity.objects.filter(
            session1_signups__lt=F('quota'))
        filtered2 = Activity.objects.filter(
            time=30).filter(session2_signups__lt=F('quota'))

        self.fields['activity1'].queryset = filtered1
        self.fields['activity2'].queryset = filtered2
