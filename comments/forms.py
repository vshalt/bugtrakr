from django import forms
from django.http import Http404
from tickets.models import Ticket
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('body',)
        labels = {'body': 'Comment'}
