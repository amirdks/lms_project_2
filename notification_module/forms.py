from django import forms

from notification_module.models import CustomNotification


class CustomNotificationForm(forms.ModelForm):
    class Meta:
        model = CustomNotification
        fields = ['title', 'text', 'base', 'field_of_study']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان اعلان...'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'متن اعلان ...'}),
            'base': forms.Select(attrs={'class': 'custom-select'}),
            'field_of_study': forms.Select(attrs={'class': 'custom-select'}),
        }
        labels = {
            'title': 'عنوان اعلان',
            'text': 'متن اعلان',
            'base': 'برای پایه',
            'field_of_study': 'برای رشته',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CustomNotificationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        m = super(CustomNotificationForm, self).save(commit=False)
        m.from_teacher = self.user
        if commit:
            m.save()
        return m
