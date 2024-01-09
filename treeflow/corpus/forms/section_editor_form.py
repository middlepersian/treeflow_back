from django import forms
from django_select2 import forms as s2forms
from treeflow.corpus.models import Section
import logging
logger = logging.getLogger(__name__)


class SenseWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "sense__icontains",
    ]


class SectionEditorForm(forms.ModelForm):
    logger.debug("SectionEditorForm")
    
    tokens_display = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'readonly': True}), required=False)
    class Meta:
        model = Section
        fields = ['text', 'number', 'identifier', 'type', 'title',
                  'language', 'source', 'previous',
                  'container', 'senses']
        widgets = {
            'senses': s2forms.ModelSelect2MultipleWidget(
                model='treeflow.dict.models.Sense', 
                search_fields=['sense__icontains'] 
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SectionEditorForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'tokens'):
            tokens = list(self.instance.tokens.all()) if self.instance.tokens.exists() else []
            self.fields['tokens_display'].initial = ', '.join(str(token) for token in tokens)
            self.fields['tokens_display'].widget.attrs['readonly'] = True
            self.fields['tokens_display'].widget.attrs['style'] = 'width: 100%;'
