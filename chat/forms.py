from django import forms

from chat.models import Chat


class ChatForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Chat Name"
        })
    )

    class Meta:
        model = Chat
        fields = ["name"]