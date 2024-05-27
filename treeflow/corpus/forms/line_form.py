from django import forms
from treeflow.corpus.models import Section, Text
import logging

logger = logging.getLogger(__name__)

class AssignLineSectionForm(forms.ModelForm):
    
    identifier = forms.ModelChoiceField(queryset=Section.objects.none(), label="Section", required=False)

    class Meta:
        model = Section
        fields = ['identifier']

    def __init__(self, *args, **kwargs):
        self.text_id = kwargs.pop('text_id', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.text_id:
            try:
                text = Text.objects.get(id=self.text_id)
                section_queryset = Section.objects.filter(text=text, type="line")
                self.fields['identifier'].queryset = section_queryset

            except Text.DoesNotExist:
                logger.debug("Text with id %s does not exist", self.text_id) 
        else:
            logger.debug("No text_id provided")        


class CreateLineSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["identifier", 'title', 'number']
