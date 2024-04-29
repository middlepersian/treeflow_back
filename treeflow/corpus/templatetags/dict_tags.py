from django import template

register = template.Library()

@register.filter
def customABCSort(data):
    custom_alphabetical_order = [
    '-', '.',
    'a', 'ā', 'ă', 'ą',
    'b',
    'c', 'ć', 'ĉ', 'ċ', 'č',
    'd', 'ď', 'đ',
    'e', 'ě', 'ē', 'ĕ', 'ė', 'ę', 'ě',
    'f',
    'g', 'ĝ', 'ğ', 'ġ', 'ģ',
    'h', 'ĥ', 'ħ',
    'i', 'ĩ', 'ī', 'ĭ', 'į', 'ı',
    'j', 'ǰ', 'ĵ',
    'k',
    'l', 'ĺ', 'ļ', 'ľ', 'ŀ', 'ł',
    'm',
    'n', 'ń', 'ņ', 'ň', 'ŋ',
    'o', 'ō', 'ŏ', 'ő',
    'p',
    'q',
    'r', 'ŕ', 'ŗ', 'ř',
    's', 'ś', 'ŝ', 'ş', 'š',
    't', 'ţ', 'ť', 'ŧ',
    'u', 'ũ', 'ū', 'ŭ', 'ů', 'ű', 'ų',
    'v',
    'w',
    'x',
    'y', 'ŷ',
    'z', 'ź', 'ż', 'ž'
]

    sorted_data = sorted(data, key=lambda x: custom_alphabetical_order.index(x.word[0]))

    return sorted_data
