from django import forms

from lesson_module.models import Lesson


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'image', 'slug', 'base', 'field_of_study', 'teacher', 'is_active']
