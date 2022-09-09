from django import forms

from poll_module.models import Poll


class CreatePollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'base', 'field_of_study', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان نظرسنجی...'}),
            'base': forms.Select(attrs={'class': 'custom-select'}),
            'field_of_study': forms.Select(attrs={'class': 'custom-select'}),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'style': 'position: relative; right:50px;'})
        }
        labels = {
            'question': 'عنوان نطرسنجی',
            'base': 'برای پایه',
            'field_of_study': 'برای رشته',
            'is_active': 'فعال',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreatePollForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        m = super(CreatePollForm, self).save(commit=False)
        m.from_teacher = self.user
        if commit:
            m.save()
        return m
