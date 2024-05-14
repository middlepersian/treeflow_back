import logging
from django import forms
from treeflow.corpus.models.section import Section
from django_select2 import forms as s2forms

# Configure logging
logger = logging.getLogger(__name__)


class SectionSelect2MultipleWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "identifier__icontains",  
    ]
        # Add custom style to the widget
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'style': 'width: 100%; min-height: 100px;'}
        super().__init__(*args, **kwargs)



class SectionForm(forms.ModelForm):
    previous = forms.ModelChoiceField(
        queryset=Section.objects.none(), required=False, label="Previous Section"
    )
    container = forms.ModelChoiceField(
        queryset=Section.objects.none(), required=False, label="Container Section"
    )
    related_to = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all(),
        widget=SectionSelect2MultipleWidget,
        required=False,
        label="Related Sections",
    )

    class Meta:
        model = Section
        fields = [
            "identifier",
            "type",
            "title",
            "source",
            "previous",
            "container",
            "related_to",
        ]

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)  # Initialize the form first
        if (
            self.instance and self.instance.pk
        ):  # Check if instance is not None and has a primary key
            self.text = self.instance.text  # Assuming 'text' is an attribute of Section
            logger.debug(f"text: {self.text}")

        if self.text:
            # filter sections based on the text
            section_queryset = Section.objects.filter(text=self.text).order_by("type")
            self.fields["previous"].queryset = section_queryset
            self.fields["container"].queryset = section_queryset
