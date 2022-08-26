import datetime
from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from jdatetime import datetime as jalali_date_time

from lesson_module.models import SetHomeWork, Lesson, PoodemanAndNobat
from lessons.models import AllowedFormats
from utils.time import end_time_calculator

now_year = datetime.datetime.now().year
now_year_jalali = jalali_date_time.now().year
YEAR_CHOICES = {
    (now_year, now_year_jalali),
    (now_year + 2, now_year_jalali + 2),
    (now_year + 1, now_year_jalali + 1),
}


class SetHomeWorkForm(forms.Form):
    title = forms.CharField(label='عنوان تکلیف',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان ...'}))
    end_at = forms.DateTimeField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
                                 label="زمان پایان مهلت")
    format = forms.ModelMultipleChoiceField(label='فرمت های مجاز',
                                            widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
                                            queryset=AllowedFormats.objects.all())
    max_size = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'custom-select', 'placeholder': 'سایز ...'}), label='حداکثر حجم فایل')
    poodeman_or_nobat = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'custom-select'}),
                                               queryset=PoodemanAndNobat.objects.all(), label='مربوط به کدام پودمان یا نوبت')
    score_weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}), label='وزن نمره')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows': '3', 'placeholder': 'توضیحات ...'}), label='توضیحات تکلیف')

    def clean_end_at(self):
        end_time = self.cleaned_data.get('end_at')
        now_time_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        now_time = datetime.datetime.strptime(now_time_str, "%m/%d/%Y %H:%M:%S")
        end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
        end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
        if now_time >= end_time:
            raise forms.ValidationError('لطفا به زمان پایان دقت فرمایید')
        return end_time


class EditHomeWorkForm(forms.ModelForm):
    class Meta:
        model = SetHomeWork
        fields = ['title', 'end_at', 'allowed_formats', 'max_size', 'description']
        widgets = {
            'end_at': forms.DateTimeInput(
                attrs={'id': 'datepicker', 'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea,
            'allowed_formats': forms.SelectMultiple(attrs={'class': 'custom-select'})
        }
