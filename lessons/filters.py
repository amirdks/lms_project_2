import django_filters as filters
from django import forms

from lesson_module.models import Lesson
from lessons.models import Base, FieldOfStudy


class LessonListResultFilter(filters.FilterSet):
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
        model = Lesson
        fields = ('base', 'field_of_study')
