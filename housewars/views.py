from django.contrib import messages
from django.db.models import Count, F, Q, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from formtools.wizard.views import SessionWizardView

from housewars.forms import ActivityForm, PointsEntryForm, UserEntryForm, FacilitatorForm
from housewars.models import Activity, Quota, PointsEntry, UserEntry, Facilitator

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
                'activity2', filter=Q(activity2__house=cd.get('user-house')))).filter(final_quota__gt=F('count'), time=30)

            # Render filtered as choices in activity select step
            form.fields['activity1'].queryset = filtered1
            form.fields['activity2'].queryset = filtered2

        return form

    def done(self, form_list, **kwargs):
        cleaned_data = self.get_all_cleaned_data()
        UserEntry.objects.create(**cleaned_data)

        activity1 = cleaned_data['activity1']
        activity2 = cleaned_data['activity2']

        # Build the response string.
        a1_string = f'You are in {activity1}'
        activity1_room = activity1.room_number

        if (activity1_room != None):
            a1_string += f' in {activity1_room}'

        if (hasattr(activity1, 'teacher')):
            activity1_teacher = activity1.teacher
            a1_string += f' with {activity1_teacher}.'
        else:
            a1_string += '.'

        a2_string = ''
        if (activity2 != None):
            a2_string = f'You are in {activity2}'

            activity2_room = activity2.room_number
            if (activity2_room != None):
                a2_string += f' in {activity2_room}'
            if (hasattr(activity2, 'teacher')):
                activity2_teacher = activity2.teacher.last_name
                a2_string += f' with {activity2_teacher}.'
            else:
                a2_string += '.'

        messages.success(self.request, 'Your signup has been submitted.')
        messages.success(self.request, a1_string)
        messages.success(self.request, a2_string)

        return redirect('housewars:signup')

    def get_success_url(self):
        return reverse('housewars:signup')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Signup'
        context['formtitle'] = 'House Wars Signup'
        return context


class PointsEntryCreateView(CreateView):
    model = PointsEntry
    form_class = PointsEntryForm
    template_name = 'housewars/general_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your points entry has been submitted.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('housewars:add_points')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Points'
        context['formtitle'] = 'Add House Points'
        return context


class FacilitatorCreateView(CreateView):
    model = Facilitator
    form_class = FacilitatorForm
    template_name = 'housewars/general_form.html'

    def form_valid(self, form):
        messages.success(
            self.request, 'Your facilitator signup has been submitted.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('housewars:add_points')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facilitator'
        context['formtitle'] = 'Facilitator Signup'
        return context
