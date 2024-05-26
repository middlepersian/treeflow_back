from django import forms
from treeflow.corpus.models import Section


class CreateLineSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['identifier', 'type']
        widgets = {
            'type': forms.HiddenInput()  # Set default type as 'line' in the view before saving
        }

class AssignLineSectionForm(forms.Form):
    line_section = forms.ModelChoiceField(queryset=Section.objects.filter(type='line'), empty_label=None)