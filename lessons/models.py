from django.conf import settings
from django.db import models


# Create your models here.


class Base(models.Model):
    BASE_TYPES = {
        ('paye_10', 'پایه دهم'),
        ('paye_11', 'پایه یازدهم'),
        ('paye_12', 'پایه دوازدهم'),
    }
    title = models.CharField(max_length=50, choices=BASE_TYPES, default='paye_10', verbose_name='عنوان پایه')
    base_number = models.IntegerField(default=10, editable=False, verbose_name='عدد پایه')

    def __str__(self):
        return self.title_farsi()

    class Meta:
        verbose_name = 'پایه'
        verbose_name_plural = "پایه ها"

    def title_farsi(self):
        if self.title == 'paye_10':
            return 'پایه دهم'
        elif self.title == 'paye_11':
            return 'پایه یازدهم'
        elif self.title == 'paye_12':
            return 'پایه دوازدهم'


class FieldOfStudy(models.Model):
    FIELD_Of_STUDY_TYPES = {
        ('Mathematical_Physics', 'ریاضی فیزیک'),
        ('Liberal_Arts', 'علوم انسانی'),
        ('Experimental_Science', 'علوم تجربی'),
        ('Software_Defined_Networking', 'شبکه و نرم افزار'),
    }
    title = models.CharField(max_length=50, choices=FIELD_Of_STUDY_TYPES, verbose_name='عنوان رشته تحصیلی')

    def __str__(self):
        return self.title_farsi()

    def title_farsi(self):
        if self.title == 'Mathematical_Physics':
            return 'ریاضی فیزیک'
        elif self.title == 'Liberal_Arts':
            return 'علوم انسانی'
        elif self.title == 'Experimental_Science':
            return 'علوم تجربی'
        else:
            return 'شبکه و نرم افزار'

    class Meta:
        verbose_name = 'رشته'
        verbose_name_plural = "رشته ها"


class AllowedFormats(models.Model):
    format = models.CharField(max_length=100, verbose_name='فرمت')

    def __str__(self):
        return self.format

    class Meta:
        verbose_name = 'فرمت'
        verbose_name_plural = 'فرمت ها'