from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password should match')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username or email', max_length=80)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {'username': 'Username', 'email': 'Email',
                  'first_name': 'First name', 'last_name': 'Last name'}


class ProfileEditForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('github',)
        help_texts = {'github': 'Enter your github username'}


class EditRolesForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=Profile.choices)

    class Meta():
        model = Profile
        fields = ('roles',)

