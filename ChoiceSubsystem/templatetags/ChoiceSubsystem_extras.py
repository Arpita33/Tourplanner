from django import template

register = template.Library()

@register.filter
def add1(val,arg):
    return int(arg*3+1)

@register.filter
def add2(val,arg):
    return arg*3+2

@register.filter
def add0(val,arg):
    return arg*3

@register.filter(name='length')
def length(dict, temp):
  return len(dict)

@register.filter(name='range')
def filter_range(start, end):
  return range(start, end)

@register.filter(name='foo')
def foo(dict, key):
    return dict[key]




