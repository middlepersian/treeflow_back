from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def render_comments_for_model(model_instance):
    model_name = model_instance._meta.model_name  # Get the model name in lowercase

    # Use the prefetched related field name for comments
    related_field_name = f'comment_{model_name}'
    comments = getattr(model_instance, related_field_name).all()

    return render_to_string('comment_data.html', {'comments': comments})
