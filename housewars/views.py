from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView

from .models import Entry
from .forms import EntryForm


class EntryCreateView(CreateView):
    form_class = EntryForm
    template_name = 'housewars/entry_form.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Your entry has been submitted')
            return super().post(request)

        messages.error(
            request, 'Please enter activities adding up to one hour.')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        prev = Entry.objects.filter(email=form.cleaned_data['email'])
        for entry in prev:
            entry.delete()

        print('form valid')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('housewars:create_entry')
