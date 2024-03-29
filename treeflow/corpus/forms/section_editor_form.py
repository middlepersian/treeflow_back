from django import forms
from django_select2 import forms as s2forms
from treeflow.corpus.models import Section
import logging
logger = logging.getLogger(__name__)


class SenseWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "sense__istartswith",  # Changed from icontains to istartswith
    ]


class SectionEditorForm(forms.ModelForm):
    logger.debug("SectionEditorForm")
    
    tokens_display = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'readonly': True}), required=False)
    class Meta:
        model = Section
        fields = ['number', 'identifier', 'type', 'title',
                  'language', 'senses']
        widgets = {
            'senses': s2forms.ModelSelect2MultipleWidget(
                model='treeflow.dict.models.Sense', 
                search_fields=['sense__istartswith'], 
                attrs={'style': 'width: 100%; min-height: 100px;'}  # Adjusted style
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SectionEditorForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'tokens'):
            tokens = list(self.instance.tokens.all()) if self.instance.tokens.exists() else []
            self.fields['tokens_display'].initial = ', '.join(str(token) for token in tokens)
            self.fields['tokens_display'].widget.attrs['readonly'] = True
            self.fields['tokens_display'].widget.attrs['style'] = 'max-height: 200px; resize: vertical; width: 100%; border-radius: 5px;'

        self.fields['number'].widget.attrs.update({
            'style': 'border-radius: 5px;',
        })
        self.fields['identifier'].widget.attrs.update({
            'style': 'border-radius: 5px;',
        })
        self.fields['type'].widget.attrs.update({
            'style': 'border-radius: 5px;',
        })
        self.fields['title'].widget.attrs.update({
            'style': 'border-radius: 5px;',
        })
        self.fields['language'].widget.attrs.update({
            'style': 'border-radius: 5px;',
        })
