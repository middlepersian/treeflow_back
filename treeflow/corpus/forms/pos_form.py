# forms.py
from django import forms
from django.forms import inlineformset_factory
from treeflow.corpus.models import POS, Token
class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ('pos', 'type')

    def __init__(self, *args, **kwargs):
        super(POSForm, self).__init__(*args, **kwargs)
        pos_choices = POS.objects.order_by('pos').values_list('pos', flat=True).distinct()
        self.fields['pos'].choices = [(pos, pos) for pos in pos_choices]

# POSFormSet to manage a collection of POS forms
POSFormSet = inlineformset_factory(
    Token, POS, form=POSForm, 
    fields=('pos', 'type'), extra=0, can_delete=True
)
