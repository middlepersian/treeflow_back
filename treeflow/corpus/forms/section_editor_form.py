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

    class Meta:
        model = Section
        fields = ['text', 'number', 'identifier', 'type', 'title',
                  'language', 'source', 'tokens', 'previous',
                  'container', 'senses']
        widgets = {
            'senses': s2forms.ModelSelect2MultipleWidget(
                model='treeflow.dict.models.Sense', 
                search_fields=['sense__icontains'] 
            ),
        }
    def __init__(self, *args, **kwargs):
        super(SectionEditorForm, self).__init__(*args, **kwargs)
