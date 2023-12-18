# create a django formset for images
from django import forms
from ..models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['identifier', 'page', 'number', 'source', 'previous']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        # Customize form widget attributes if needed
        self.fields['identifier'].widget.attrs.update({'class': 'form-control'})
        self.fields['page'].widget.attrs.update({'class': 'form-control'})
        self.fields['number'].widget.attrs.update({'class': 'form-control'})
        self.fields['source'].widget.attrs.update({'class': 'form-control'})
        self.fields['previous'].widget.attrs.update({'class': 'form-control'})
