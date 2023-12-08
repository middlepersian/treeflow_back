from django import forms
from django.forms import inlineformset_factory
from treeflow.corpus.models import POS, Token

class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ('pos', 'type')
        widgets = {
            'type': forms.HiddenInput(),  # Makes the type field hidden
        }

    def __init__(self, *args, **kwargs):
        super(POSForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = 'upos'  # Sets a default value for type

# POSFormSet to manage a collection of POS forms
POSFormSet = inlineformset_factory(
    Token, POS, form=POSForm,
    fields=('pos', 'type'),  # Specify the fields here, the type will be included but hidden
        can_delete=True,  # No delete checkbox
    extra=1,  # No extra forms
)
