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
        ('none', 'No Reference Section'),  # Added option for no reference section
    ]
    insertion_method = forms.ChoiceField(choices=INSERTION_CHOICES, required=True, initial='none')

    # Make reference_section optional
    reference_section = forms.ModelChoiceField(queryset=Section.objects.all(), required=False)

    # Add a field for selecting related sections
    related_sections = forms.ModelMultipleChoiceField(queryset=Section.objects.all(), required=False)

    class Meta:
        model = Section
        fields = ['identifier', 'type', 'title', 'source', 'container', 
                  'reference_section', 'insertion_method', 'related_sections']

    def __init__(self, *args, **kwargs):
        self.text_id = kwargs.pop('text_id', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.text_id:
            try:
                text = Text.objects.get(id=self.text_id)
                section_queryset = Section.objects.filter(text=text).order_by('type')
                self.fields['container'].queryset = section_queryset
                self.fields['reference_section'].queryset = section_queryset
                self.fields['related_sections'].queryset = section_queryset
            except Text.DoesNotExist:
                logger.debug("Text with id %s does not exist", self.text_id) 
        else:
            logger.debug("No text_id provided")        

    def clean(self):
        cleaned_data = super().clean()
        selected_tokens = cleaned_data.get('selected_tokens')

    def save(self, commit=True):
        insertion_method = self.cleaned_data.get('insertion_method')
        reference_section = self.cleaned_data.get('reference_section')
        selected_token_ids = self.cleaned_data.get('selected_tokens').split(',')
        related_sections = self.cleaned_data.get('related_sections')

        text = Text.objects.get(id=self.text_id) if self.text_id else Text.objects.first()
        new_section_data = {
            'identifier': self.cleaned_data.get('identifier'),
            'type': self.cleaned_data.get('type'),
            'title': self.cleaned_data.get('title'),
            'source': self.cleaned_data.get('source'),
            'container': self.cleaned_data.get('container'),
            'text': text,        }

        if insertion_method == 'before' and reference_section:
            new_section = Section.insert_before(reference_section.id, new_section_data, user=self.user)
        elif insertion_method == 'after' and reference_section:
            new_section = Section.insert_after(reference_section.id, new_section_data, user=self.user)
        else:
            new_section = Section(**new_section_data)
            if commit:
                new_section.save()

        if selected_token_ids:
            for token_id in selected_token_ids:
                try:
                    token = Token.objects.get(id=token_id)
                    new_section.tokens.add(token)
                except Token.DoesNotExist:
                    logger.error(f"Token with ID {token_id} does not exist")

        # Add the related sections
        for section in related_sections:
            new_section.related_to.add(section)

        return new_section
