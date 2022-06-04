from django import forms


class SendHomeWorkForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(), label='فایل')
