from django import forms

class SendMessageForm(forms.Form):
    message_text = forms.CharField(widget=forms.TextInput(attrs={'rows': '3'}))

