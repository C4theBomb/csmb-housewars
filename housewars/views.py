from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from .models import Entry
from .forms import EntryForm


class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm

    def get_success_url(self):
        return reverse('housewars:create_entry')
