from django import forms
from treeflow.corpus.models import Section
import logging
logger = logging.getLogger(__name__)

class SectionEditorForm(forms.ModelForm):
    logger.debug("SectionEditorForm")
    class Meta:
        model = Section
        fields = ['text', 'number', 'identifier', 'type', 'title', 
                  'language', 'source', 'tokens', 'previous', 
                  'container', 'senses']

    def __init__(self, *args, **kwargs):
        super(SectionEditorForm, self).__init__(*args, **kwargs)

