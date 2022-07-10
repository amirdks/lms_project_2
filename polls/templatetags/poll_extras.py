from django import template
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
