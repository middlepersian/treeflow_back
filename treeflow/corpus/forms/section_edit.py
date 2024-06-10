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
        kwargs["attrs"] = {"style": "width: 100%; min-height: 100px;"}
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
    tokens_display = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "readonly": True}),
        required=False,
        label="Tokens",
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
            if self.instance and hasattr(self.instance, "tokens"):
                tokens = (
                    list(self.instance.tokens.all())
                    if self.instance.tokens.exists()
                    else []
                )
                self.fields["tokens_display"].initial = " ".join(
                    str(token) for token in tokens
                )
                self.fields["tokens_display"].widget.attrs["readonly"] = True
                # disable tokens as input field
                self.fields["tokens_display"].widget.attrs["disabled"] = True
                self.fields["tokens_display"].widget.attrs["style"] = (
                    "max-height: 200px; resize: vertical; width: 100%; border-radius: 5px;"
                )

                self.text = (
                    self.instance.text
                )  # Assuming 'text' is an attribute of Section

                if self.text:
                    # filter sections based on the text
                    logger.info(f"Filtering sections based on text: {self.text}")

                    section_queryset = Section.objects.filter(text=self.text).order_by(
                        "type"
                    )
                    self.fields["previous"].queryset = section_queryset
                    self.fields["container"].queryset = section_queryset
                    self.fields["related_to"].queryset = section_queryset
                    # log that the sections have been filtered
                    logger.info(
                        f"Sections filtered based on text: {self.text} - {section_queryset.count()} sections found."
                    )
