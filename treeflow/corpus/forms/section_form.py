
from django import forms
from treeflow.corpus.models.section import Section

class SectionForm(forms.ModelForm):
    selected_tokens = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Section
        fields = ['identifier', 'type', 'title', 'language', 'number', 'source', 'previous', 'container', 'senses']
        # Add other fields as needed

        widgets = {
            'identifier': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'type': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'container': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            # Define widgets for other fields similarly
        }
