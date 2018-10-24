from django import template
from django.utils.timezone import now
from datetime import datetime


register = template.Library()
@register.filter
def data_format(val):
    if not isinstance(val,datetime):
        return val
    time_now = now()
    sec = (time_now-val).total_seconds()
    if sec < 60:
        return "{}".format("刚刚")
    elif 60 <= sec <60 *60:
        mint = int(sec / 60)
        return "{}分钟前".format(mint)
    elif 60*60 <= sec < 60*60*24:
        hour = int(sec/60/60)
        return "{}小时前".format(hour)
    elif 60*60*24 <= sec <60*60*24*2:
        return "昨天"
    else:
        return val.strftime("%Y/%m%d:%H:%M")
