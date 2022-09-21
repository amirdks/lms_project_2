import json

from django import template
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from jalali_date import date2jalali, datetime2jalali

register = template.Library()


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='show_jalali_date_time')
def show_jalali_date_time(value):
    return datetime2jalali(value)


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return '{:,}'.format(value) + ' تومان'


@register.filter(name='index')
def index(indexable, i):
    return indexable[i]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def in_homework(send_homework, set_homework_id):
    return send_homework.filter(home_work_id=set_homework_id)


@register.filter(name='dont_show_none')
def dont_show_none(value):
    if value is None:
        return '____'
    return value


@register.filter(name='file_name')
def file_name(value):
    return str(value).split('/')[-1]


@register.filter(name='to_json')
def to_json(value):
    data = list(value.values('id', 'username', 'first_name', 'last_name'))
    return json.dumps(data)


@register.filter(name='change_month')
def change_month(date):
    jmonth = {
        "01": "فروردین",
        "02": "اردیبهشت",
        "03": "خرداد",
        "04": "تیر",
        "05": "مرداد",
        "06": "شهریور",
        "07": "مهر",
        "08": "آبان",
        "09": "آذر",
        "10": "دی",
        "11": "بهمن",
        "12": "اسفند",
    }
    date = str(date).replace("-", " ")
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    for e, p in jmonth.items():
        month = month.replace(e, p)
    return f"{day} {month} {year}"


@register.filter(name='persian_number_converter')
def persian_number_converter(my_str):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        my_str = my_str.replace(e, p)
    return my_str
