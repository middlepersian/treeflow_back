from django import forms
from django.forms import modelformset_factory
from treeflow.corpus.models.comment import Comment
from django.core.validators import RegexValidator


class SingleCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1
        kwargs['validators'] = [RegexValidator(
            r'^[A-Z]$', 'Only uppercase characters are allowed')]
        super(SingleCharField, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):
    related_model_id = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial=None)
    related_model_type = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['comment', 'related_model_id', 'related_model_type',
                  'uncertain', 'to_discuss', 'new_suggestion']

    def __init__(self, *args, **kwargs):
        related_model_type = kwargs.pop('related_model_type', None)
        related_model_id = kwargs.pop('related_model_id', None)
        super().__init__(*args, **kwargs)

        self.fields['related_model_type'].initial = related_model_type
        self.fields['related_model_id'].initial = related_model_id

        if related_model_type == 'Token':
            self.fields['uncertain'] = SingleCharField(
                widget=forms.TextInput(), required=False)
            self.fields['to_discuss'] = SingleCharField(
                widget=forms.TextInput(), required=False)
            self.fields['new_suggestion'] = SingleCharField(
                widget=forms.TextInput(), required=False)

        def clean_uncertain(self):
            data = self.cleaned_data.get('uncertain', '')
            if isinstance(data, str):
                return list(filter(None, data.upper().split(',')))
            return data  # Already a list or another type, return as is

        def clean_to_discuss(self):
            data = self.cleaned_data.get('to_discuss', '')
            if isinstance(data, str):
                return list(filter(None, data.upper().split(',')))
            return data

        def clean_new_suggestion(self):
            data = self.cleaned_data.get('new_suggestion', '')
            if isinstance(data, str):
                return list(filter(None, data.upper().split(',')))
            return data


# Usage of formset in your view
CommentFormSet = modelformset_factory(
    Comment, form=CommentForm, extra=1, can_delete=True)
