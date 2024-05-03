from django import template

register = template.Library()

@register.filter
def next(list, current_index):
    try:
        return list[int(current_index) + 1] # access the next element
    except:
        return '' # return empty string in case of exception

@register.filter
def previous(list, current_index):
    try:
        return list[int(current_index) - 1] # access the previous element
    except:
        return '' # return empty string in case of exception
