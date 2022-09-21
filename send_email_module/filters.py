import django_filters as filters
from django import forms

from lessons.models import Base
from send_email_module.models import Email


class QuizResultFilter(filters.FilterSet):
    base = filters.ModelChoiceFilter(
        queryset=Base.objects.all(),
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            'class': 'form-control'
        }),
    )

    class Meta:
        model = Email
        fields = ('base',)
