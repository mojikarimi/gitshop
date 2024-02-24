from django import template
from jdatetime import datetime,date
register = template.Library()


def filter_text(value, arg: None):
    if len(value) >= arg:
        value = value[:arg] + '...'
    return value


register.filter('filter_text', filter_text)


def filter_date(value, arg: None):
    return value[:arg]


register.filter('filter_date', filter_date)





def filter_date_difference(value, arg= None):
    if value:
        print(type(value))
        year = value[:4]
        month = value[5:7]
        day = value[8:10]
        value = str(date(int(year), int(month), int(day)).togregorian())
        year = value[:4]
        month = value[5:7]
        day = value[8:10]
        value=f'{month} {day} {year}'
    return value


register.filter('filter_date_difference', filter_date_difference)
