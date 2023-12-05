from django import forms
from ..models import Source, BibEntry

class BibEntryForm(forms.ModelForm):
    class Meta:
        model = BibEntry
        fields = ['key']

class SourceForm(forms.ModelForm):
    bibentry_forms = forms.formset_factory(BibEntryForm, extra=1, can_delete=True)

    class Meta:
        model = Source
        fields = ['type', 'identifier', 'description', 'references', 'sources']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bibentry_forms = self.bibentry_forms(*args, **kwargs)

    def is_valid(self):
        return super().is_valid() and self.bibentry_forms.is_valid()

    def save(self, commit=True):
        source_instance = super().save(commit)
        for bibentry_form in self.bibentry_forms:
            if bibentry_form.cleaned_data and not bibentry_form.cleaned_data.get('DELETE', False):
                key = bibentry_form.cleaned_data['key']
                b = BibEntry.objects.create(key=key)
                b.save()
                source_instance.references.add(b)
                source_instance.save()
        return source_instance
