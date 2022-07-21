from django import forms


class SendHomeWorkForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False ,label='پیام به معلم')
