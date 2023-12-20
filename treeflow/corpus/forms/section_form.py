from django import forms
from treeflow.corpus.models.section import Section
from treeflow.corpus.models.text import Text
from treeflow.corpus.models.token import Token
import logging

logger = logging.getLogger(__name__)


class SectionForm(forms.ModelForm):
    selected_tokens = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Define choices for insertion method
    INSERTION_CHOICES = [
        ('before', 'Before Reference Section'),
        ('after', 'After Reference Section'),
    ]
    insertion_method = forms.ChoiceField(choices=INSERTION_CHOICES, required=True)

    # Add a field for selecting the reference section
    reference_section = forms.ModelChoiceField(queryset=Section.objects.all(), required=True)

    class Meta:
        model = Section
        fields = ['identifier', 'type', 'title', 
                  'source', 'container', 'reference_section', 'insertion_method' ]

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
                # set reference_section queryset
                self.fields['reference_section'].queryset = Section.objects.filter(text=text).exclude(type__in=['sentence', 'line']).order_by('type')
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
        logger.debug("Starting to save new section")

        insertion_method = self.cleaned_data.get('insertion_method')
        reference_section = self.cleaned_data.get('reference_section')
        selected_token_ids = self.cleaned_data.get('selected_tokens').split(',')

        logger.debug(f"Insertion Method: {insertion_method}")
        logger.debug(f"Reference Section ID: {reference_section.id if reference_section else 'None'}")
        logger.debug(f"Selected Token IDs: {selected_token_ids}")

        # Prepare new section data from cleaned_data
        new_section_data = {
            'identifier': self.cleaned_data.get('identifier'),
            'type': self.cleaned_data.get('type'),
            'title': self.cleaned_data.get('title'),
            'language': self.cleaned_data.get('language'),
            'source': self.cleaned_data.get('source'),
            'container': self.cleaned_data.get('container'),
            'text': reference_section.text,        }

        if insertion_method == 'before':
            new_section = Section.insert_before(reference_section.id, new_section_data)
        elif insertion_method == 'after':
            new_section = Section.insert_after(reference_section.id, new_section_data)
        else:
            new_section = super().save(commit=commit)

        logger.debug(f"New section created: {new_section.id} - {new_section.identifier}")

        # Associate selected tokens with the new section, if any
        if selected_token_ids:
            for token_id in selected_token_ids:
                try:
                    token = Token.objects.get(id=token_id)
                    new_section.tokens.add(token)
                    logger.debug(f"Token {token_id} added to section {new_section.id}")
                except Token.DoesNotExist:
                    logger.error(f"Token with ID {token_id} does not exist")

        return new_section
