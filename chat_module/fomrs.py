import os

from django import forms


class FileMessageForm(forms.Form):
    file_message = forms.FileField(widget=forms.FileInput, error_messages={'required': 'حتما باید فایلی را ارسال کنید'})

    def clean_file_message(self):
        f = self.cleaned_data.get('file_message')
        value = round(f.size / 1000000, 2)
        if not os.path.splitext(f.__str__())[-1].lower() in ['.rar', '.zip', '.jpeg', '.jpg', '.png', '.pdf']:
            raise forms.ValidationError(
                'نمیتونی فایل {} با فرمت {} رو بفرستی'.format(f.__str__(), os.path.splitext(f.__str__())[-1].lower()))
        elif value > 25:
            raise forms.ValidationError('حجم فایل ارسال شده بالاتر از حد مجاز است')
        return f
