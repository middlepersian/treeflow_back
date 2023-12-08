from django import forms
from django.contrib.auth import get_user_model
from django.contrib.postgres.forms import SimpleArrayField
from treeflow.corpus.models import Text, Source

User = get_user_model()

class TextForm(forms.ModelForm):
    language = SimpleArrayField(forms.CharField(max_length=100), delimiter=',')    
    editors = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    collaborators = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    sources = forms.ModelMultipleChoiceField(queryset=Source.objects.all(), required=False)

    class Meta:
        model = Text
        fields = ['title', 'identifier', 'language', 'series', 'label', 'version', 'stage', 'corpus', 'editors', 'collaborators', 'sources']
        widgets = {
            'corpus': forms.Select(),
        }
