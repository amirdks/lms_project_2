from django import forms


class SendHomeWorkForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(), label='فایل')
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='پیام به معلم')
