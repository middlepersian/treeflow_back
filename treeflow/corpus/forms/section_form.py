from django import forms
from treeflow.corpus.models.section import Section

import logging

logger = logging.getLogger(__name__)


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['identifier']