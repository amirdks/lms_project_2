from django import forms
import django_filters as filters

from account_module.models import User
from lessons.models import Base, FieldOfStudy


class StudentListResultFilter(filters.FilterSet):
    base = filters.ModelChoiceFilter(
        queryset=Base.objects.all(),
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            'class': 'form-control'
        }),
    )
    field_of_study = filters.ModelChoiceFilter(
        queryset=FieldOfStudy.objects.all(),
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            'class': 'form-control'
        }),
    )

    class Meta:
        model = User
        fields = ('base', 'field_of_study')
