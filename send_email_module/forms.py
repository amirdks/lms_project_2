from django import forms

from send_email_module.models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        exclude = ['from_teacher']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موضوع ایمیل...'}),
            'field_of_study': forms.Select(attrs={'class': 'custom-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'متن ایمیل ...'}),
            'base': forms.Select(attrs={'class': 'custom-select'}),
            'send_at': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'})
        }
        error_messages = {
            'subject': {
                'required': "فیلد موضوع ایمیل نمیتواند خالی باشد",
            },
            'field_of_study': {
                'required': "فیلد رشته نمیتواند خالی باشد",
            },
            'content': {
                'required': "فیلد متن ایمیل نمیتواند خالی باشد",
            },
            'base': {
                'required': "فیلد پایه نمیتواند خالی باشد",
            },
        }
        labels = {
            'subject': 'موضوع ایمیل',
            'base': 'برای پایه',
            'field_of_study': 'برای رشته',
            'content': 'متن ایمیل',
            'send_at': 'ارسال در تاریخ',
        }

    def __init__(self, user=None, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        m = super(EmailForm, self).save(commit=False)
        m.from_teacher = self.user
        if commit:
            m.save()
        return m
