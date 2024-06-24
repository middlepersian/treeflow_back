from django import forms

from treeflow.corpus.enums.text_stage import TextStage


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
            'class': 'text-center rounded-md',
            'onchange': 'updateInput(this)'
        })
        return super().render(name, value, attrs, renderer)

class TextStageForm(forms.Form):
    stage = forms.ChoiceField(
        choices=[(stage.name, stage.value) for stage in TextStage],
        widget=HTMXSelectWidget(),
    )

    def __init__(self, *args, **kwargs):
        hx_post_url = kwargs.pop('hx_post_url', '')
        csrf_token = kwargs.pop('csrf_token', '')
        super().__init__(*args, **kwargs)
        self.fields['stage'].widget = HTMXSelectWidget(
            hx_post_url=hx_post_url,
            csrf_token=csrf_token,
            choices=self.fields['stage'].choices
        )