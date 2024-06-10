from django import forms
from treeflow.corpus.enums.text_genre import TextGenre

class HTMXSelectWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        self.hx_post_url = kwargs.pop('hx_post_url', '')
        self.csrf_token = kwargs.pop('csrf_token', '')
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs.update({
            'hx-post': self.hx_post_url,
            'hx-trigger': 'change',
            'hx-headers': f'{{"X-CSRFToken": "{self.csrf_token}"}}',
            'hx-swap': 'none',
            'class': 'text-center rounded-md'
        })
        return super().render(name, value, attrs, renderer)

class TextGenreForm(forms.Form):
    label = forms.ChoiceField(
        choices=[(label.name, label.value) for label in TextGenre],
        widget=HTMXSelectWidget(),
    )

    def __init__(self, *args, **kwargs):
        hx_post_url = kwargs.pop('hx_post_url', '')
        csrf_token = kwargs.pop('csrf_token', '')
        super().__init__(*args, **kwargs)
        self.fields['label'].widget = HTMXSelectWidget(
            hx_post_url=hx_post_url,
            csrf_token=csrf_token,
            choices=self.fields['label'].choices
        )