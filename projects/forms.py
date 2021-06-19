from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ('title', 'description')
        widgets = {
            'description': forms.Textarea
        }


class AddUserForm(forms.Form):
    def __init__(self, project_users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned'] = forms.ModelMultipleChoiceField(project_users)
        self.fields['assigned'].label = 'Assigned users'
        self.fields['assigned'].required = False


class RemoveUserForm(forms.Form):
    def __init__(self, all_users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['all_users'] = forms.ModelMultipleChoiceField(all_users)
        self.fields['all_users'].label = 'All users'
        self.fields['all_users'].required = False
