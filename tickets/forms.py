from django import forms
from django.http import Http404

from accounts.models import Profile
from projects.models import Project
from .models import Ticket, TicketHistory
from common.utils import send_ticket_update_email, get_user_roles


class TicketCreateForm(forms.ModelForm):
    def __init__(self, project_id, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.profile = request.user.profile
        self.initial_title = self.instance.title
        self.initial_description = self.instance.description
        self.initial_classification = self.instance.classification
        self.initial_status = self.instance.status
        self.initial_priority = self.instance.priority
        self.user, self.roles = get_user_roles(request)
        self.fields['project'].queryset = Project.objects.filter(
            users__id=request.user.profile.id)
        self.fields['project'].empty_label = 'Select a project'
        if ('admin' in self.roles or 'manager' in self.roles
            or self.user.is_superuser):
            pass
        else:
            self.fields.pop('status')
            self.fields.pop('priority')
        try:
            self.initial_project = self.instance.project
        except:
            self.initial_project = None
        if self.initial_project is None:
            # self.fields['status'].widget = forms.HiddenInput()
            pass

    def save(self, commit=True):
        instance = super().save(commit=True)
        if not instance.owner:
            instance.owner = self.profile
            instance.save()
        if self.initial_project is None:
            TicketHistory.objects.create(
                ticket=self.instance, user=self.profile,
                message=(
                    f"Ticket created:\n"
                    f"Title: {self.instance.title}\n"
                    f"Project: {self.instance.project}\n"
                    f"Description: {self.instance.description}\n"
                    f"Priority: {self.instance.priority}"))
        else:
            if self.has_changed():
                for change in self.changed_data:
                    if change == 'title':
                        TicketHistory.objects.create(
                            user=self.profile, ticket=self.instance, message=(
                                f"Title changed from '{self.initial_title}'"
                                f"to '{self.instance.title}'"))
                    if change == 'description':
                        TicketHistory.objects.create(
                            user=self.profile, ticket=self.instance, message=(
                                f"Description changed from"
                                f"'{self.initial_description}' to "
                                f"'{self.instance.description}'"))
                    if change == 'project':
                        TicketHistory.objects.create(
                            user=self.profile, ticket=self.instance, message=(
                                f"Project changed from '{self.initial_project}'"
                                f"to '{self.instance.project}'"))
                    if change == 'classification':
                        TicketHistory.objects.create(
                            user=self.profile, ticket=self.instance, message=(
                                f"Type changed from '{self.initial_classification}'"
                                f"to '{self.instance.classification}'"))
                    if change == 'priority':
                        TicketHistory.objects.create(
                            user=self.profile, ticket=self.instance, message=(
                                f"Priority changed from '{self.initial_priority}'"
                                f"to '{self.instance.priority}'"))
                    if change == 'status':
                        TicketHistory.objects.create(
                            user=self.profile, ticket=self.instance, message=(
                                f"Status changed from '{self.initial_status}'"
                                f"to '{self.instance.status}'"))
        if commit:
            if self.profile is not instance.assigned_user and \
                    instance.assigned_user is not None:
                link = self.request.build_absolute_uri(
                    self.instance.get_absolute_url())
                send_ticket_update_email(link, self.profile, self.instance)
            instance.save()
        return instance

    class Meta():
        model = Ticket
        fields = ('title', 'description', 'project', 'classification',
                  'status', 'priority')


class TicketAssignForm(forms.Form):
    def __init__(self, request, ticket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.ticket = ticket
        if self.ticket.assigned_user:
            self.fields['assigned_user'].initial = self.ticket.assigned_user.id
    queryset = Profile.objects.filter(roles__contains='developer')
    assigned_user = forms.ModelChoiceField(
        queryset=queryset, empty_label='Select a user')
