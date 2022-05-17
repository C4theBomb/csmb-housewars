from django.shortcuts import render
from django.views.generic import CreateView

from .models import Entry


class EntryCreateView(CreateView):
    model = Entry
    fields = ['first_name', 'last_name', 'email',
              'grade', 'activity1', 'activity2']
