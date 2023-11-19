from django import forms
from treeflow.corpus.models.section import Section
from treeflow.corpus.models.text import Text
import logging

logger = logging.getLogger(__name__)


class SectionForm(forms.ModelForm):
    selected_tokens = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Define choices for insertion method
    INSERTION_CHOICES = [
        ('before', 'Insert Before Selected Section'),
        ('after', 'Insert After Selected Section'),
    ]
    insertion_method = forms.ChoiceField(choices=INSERTION_CHOICES, required=True)

    # Add a field for selecting the reference section
    reference_section = forms.ModelChoiceField(queryset=Section.objects.all(), required=True)

    class Meta:
        model = Section
        fields = ['identifier', 'type', 'title', 'language', 'number',
                  'source', 'container', 'insertion_method', 'reference_section']
        # Define widgets for other fields...

    def __init__(self, *args, **kwargs):
        text_id = kwargs.pop('text_id', None)
        logger.debug("Initializing SectionForm with text_id: %s", text_id)  #
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if text_id:
            try:
                text = Text.objects.get(id=text_id)
                container_queryset = Section.objects.filter(text=text).exclude(type__in=['sentence', 'line']).order_by('type')
                self.fields['container'].queryset = container_queryset
                logger.debug("Container QuerySet: %s", container_queryset.query)  # Debugging statement
            except Text.DoesNotExist:
                # Handle the case where text does not exist
                logger.debug("Text with id %s does not exist", text_id) 
        else:   
            # Handle the case where text_id is not provided
            logger.debug("No text_id provided")        


    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic...
        selected_tokens = cleaned_data.get('selected_tokens')
        logger.debug("SectionForm: selected_tokens: %s", selected_tokens)

    def save(self, commit=True):
        insertion_method = self.cleaned_data.get('insertion_method')
        reference_section = self.cleaned_data.get('reference_section')

        new_section_data = {
            # Prepare new section data...
        }

        if insertion_method == 'before':
            new_section = Section.insert_before(reference_section.id, new_section_data)
        elif insertion_method == 'after':
            new_section = Section.insert_after(reference_section.id, new_section_data)
        else:
            new_section = super().save(commit=commit)

        return new_section
