from django import template

register = template.Library()

@register.simple_tag
def highlight_if_match(section_token_transcription, queries):
    if not section_token_transcription or not queries:
        return 'text-red-500'
    
    for query in queries:
        if query in section_token_transcription:
            return 'text-off font-bold'
    return ''