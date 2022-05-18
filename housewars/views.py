from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from .models import Entry
from .forms import EntryForm


class EntryCreateView(FormView):
    form_class = EntryForm
    template_name = 'housewars/entry_form.html'

    def form_valid(self, form):
        prev = Entry.objects.filter(email=form.cleaned_data['email'])
        for entry in prev:
            entry.delete()

        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('housewars:create_entry')
