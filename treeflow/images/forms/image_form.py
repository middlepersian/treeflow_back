from django import forms
from django.forms import modelformset_factory
from ..models import Image
from treeflow.corpus.models import Source

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        # Customize the 'source' field to be a dropdown of available sources
        self.fields['source'].queryset = Source.objects.all()

ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)