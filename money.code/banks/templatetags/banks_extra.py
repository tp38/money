from django import template
from money.settings import MONEY_DATE, MONEY_VERSION

register = template.Library()

@register.filter
def get_slug(BA):
    return BA.Slug()

@register.filter
def own_by(BA):
    return BA.own_by()

@register.filter
def get_two_digit(month):
    if int(month) < 10 :
        return f"{month:02}"
    else:
        return f"{month}"

@register.simple_tag
def app_version():
    return MONEY_VERSION

@register.simple_tag
def app_date():
    return MONEY_DATE
