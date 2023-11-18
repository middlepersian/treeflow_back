
from django import forms
from treeflow.corpus.models.section import Section
import logging
logger = logging.getLogger(__name__)
class SectionForm(forms.ModelForm):
    selected_tokens = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Section
        fields = ['identifier', 'type', 'title', 'language', 'number', 'source', 'previous', 'container']
        # Add other fields as needed

        widgets = {
            'identifier': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'type': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            # Define widgets for other fields similarly
        }

    def __init__(self, *args, **kwargs):
        # Optionally, you can pass additional context or parameters to the form
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter 'previous' field based on specific criteria
        self.fields['previous'].queryset = Section.objects.exclude(type__in=['sentence', 'line']).order_by('type')
        # Filter 'container' field based on specific criteria
        self.fields['container'].queryset = Section.objects.exclude(type__in=['sentence', 'line']).order_by('type')
    
    def clean(self):
        cleaned_data = super().clean()
        selected_tokens = cleaned_data.get('selected_tokens')
        logger.debug("SectionForm: selected_tokens: %s", selected_tokens)