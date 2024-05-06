from django import template

register = template.Library()

@register.filter
def customABCSort(data):
    custom_alphabetical_order = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '-', '.', ',', ';', '!', '"', '’', "'", 'ʾ', 'ʿ', '#', '$', '%', '&', '(', ')', '*', '+', '/', '\\', '|', ':', '=', '?', '@', '[', ']', '^', '_', '`', '{', '}', '~', 
    '<', '>', '¡', '¿', '€', '£', '¥', '¢', '§', '©', '®', '™', '°', '¹', '²', '³', '¼', '½', '¾', '⅓', '⅔', '⅛', '⅜', '⅝', '⅞', '∞', '√', '∑', '∆', '∫', '†',
    'a', 'ā', 'ă', 'ą',
    'b',
    'c', 'ć', 'ĉ', 'ċ', 'č',
    'd', 'ď', 'đ',
    'e', 'ě', 'ē', 'ĕ', 'ė', 'ę', 'ě',
    'f',
    'g', 'ǧ', 'ĝ', 'ğ', 'ġ', 'ģ',
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
    's', 'ṣ', 'ś', 'ŝ', 'ş', 'š',
    't', 'ţ', 'ť', 'ŧ',
    'u', 'ũ', 'ū', 'ŭ', 'ů', 'ű', 'ų',
    'v',
    'w',
    'x',
    'y', 'ẏ', 'γ', 'ŷ',
    'z', 'ẕ', 'ź', 'ż', 'ž',
    'ϑ'
]
    
    try:
        sorted_data = sorted([x for x in data.values() if x['word'] != ""], key=lambda x: custom_alphabetical_order.index(x['word'][0].lower()) if x['word'][0].lower() in custom_alphabetical_order else len(custom_alphabetical_order))
    except Exception as e:
        print(f"dict_tags error occurred: {e}")
       
        sorted_data = []
        
    return sorted_data
