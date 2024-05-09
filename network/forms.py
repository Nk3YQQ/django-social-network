from django import forms

from network.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
