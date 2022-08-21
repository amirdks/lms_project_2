import os

from django import forms
from django.core.exceptions import ValidationError

from lesson_module.models import SetHomeWork


class SendHomeWorkForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False,
                              label='پیام به معلم')
    file = forms.FileField(widget=forms.FileInput, error_messages={'required': 'حتما باید فایلی را ارسال کنید'})

    def __init__(self, home_work=None, allowed_formats=None, *args, **kwargs):
        super(SendHomeWorkForm, self).__init__(*args, **kwargs)
        self.home_work = home_work
        self.allowed_formats = allowed_formats

    def clean_file(self):
        f = self.cleaned_data.get('file')
        value = round(f.size / 1000000, 2)
        if not os.path.splitext(f.__str__())[-1].lower() in self.allowed_formats:
            raise forms.ValidationError(
                'نمیتونی فایل {} با فرمت {} رو بفرستی'.format(f.__str__(), os.path.splitext(f.__str__())[-1].lower()))
        elif value > self.home_work.max_size:
            raise forms.ValidationError('حجم فایل ارسال شده بالاتر از حد مجاز است')
        return f
