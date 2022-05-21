from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Q, F
from formtools.wizard.views import SessionWizardView

from .models import Activity, UserEntry
from .forms import UserEntryForm, ActivityForm

FORMS = [("user", UserEntryForm),
         ("activity", ActivityForm)]

TEMPLATES = {"user": "housewars/entry_form.html",
             "activity": "housewars/activity_form.html"}


class EntryCreateView(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def post(self, *args, **kwargs):
        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        if not form.is_valid():
            if (form.errors.as_data().get('__all__')):
                for error in form.errors.as_data().get('__all__'):
                    messages.error(self.request, error.messages[0])

        return super().post(*args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        if step == 'activity':
            cd = self.storage.get_step_data('user')

            filtered1 = Activity.objects.annotate(count=Count(
                'activity1', filter=Q(activity1__house=cd.get('user-house')))).filter(quota__gt=F('count'))
            filtered2 = Activity.objects.annotate(count=Count(
                'activity2', filter=Q(activity2__house=cd.get('user-house')))).filter(quota__gt=F('count'), time=30)

            form.fields['activity1'].queryset = filtered1
            form.fields['activity2'].queryset = filtered2

        return form

    def done(self, form_list, **kwargs):
        UserEntry.objects.create(**self.get_all_cleaned_data())

        messages.success(self.request, 'Your entry has been submitted')
        return redirect('housewars:create_entry')

    def get_success_url(self):
        return reverse('housewars:create_entry')
