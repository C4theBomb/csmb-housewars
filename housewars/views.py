from django.contrib import messages
from django.db.models import Count, F, Q, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from formtools.wizard.views import SessionWizardView

from .forms import ActivityForm, PointsEntryForm, UserEntryForm
from .models import Activity, Quota, PointsEntry, UserEntry

FORMS = [("user", UserEntryForm),
         ("activity", ActivityForm)]

TEMPLATES = {"user": "housewars/entry_form.html",
             "activity": "housewars/activity_form.html"}


class EntryCreateView(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        if step == 'activity':
            cd = self.storage.get_step_data('user')

            # Retrieve custom quotas for house activities
            quota = Quota.objects.filter(
                house=cd.get('user-house'), activity=OuterRef('id')).values('quota')

            # Set quota to custom quota or default, then set count to the total signups for each activity. Filter where quota is less than house signups.
            filtered1 = Activity.objects.annotate(final_quota=Coalesce(Subquery(quota[:1]), F('default_quota'))).annotate(count=Count(
                'activity1', filter=Q(activity1__house=cd.get('user-house')))).filter(final_quota__gt=F('count'))

            filtered2 = Activity.objects.annotate(final_quota=Coalesce(Subquery(quota[:1]), F('default_quota'))).annotate(count=Count(
                'activity1', filter=Q(activity2__house=cd.get('user-house')))).filter(final_quota__gt=F('count'), time=30)

            # Render filtered as choices in activity select step
            form.fields['activity1'].queryset = filtered1
            form.fields['activity2'].queryset = filtered2

        return form

    def done(self, form_list, **kwargs):
        UserEntry.objects.create(**self.get_all_cleaned_data())

        messages.success(self.request, 'Your signup has been submitted.')
        return redirect('housewars:signup')

    def get_success_url(self):
        return reverse('housewars:signup')


class PointsEntryCreateView(CreateView):
    model = PointsEntry
    form_class = PointsEntryForm

    def form_valid(self, form):
        messages.success(self.request, 'Your points entry has been submitted.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('housewars:add_points')
