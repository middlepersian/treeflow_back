from django import forms
from django_select2 import forms as s2forms
from treeflow.corpus.models.section import Section
from treeflow.corpus.models.text import Text
from treeflow.corpus.models.token import Token
import logging

logger = logging.getLogger(__name__)


class SectionForm(forms.ModelForm):
    selected_tokens = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Define choices for insertion method
    INSERTION_CHOICES = [
        ("before", "Before Reference Section"),
        ("after", "After Reference Section"),
        ("none", "No Reference Section"),  # Added option for no reference section
    ]
    insertion_method = forms.ChoiceField(
        choices=INSERTION_CHOICES, required=True, initial="none"
    )

    # Make reference_section optional
    reference_section = forms.ModelChoiceField(
        queryset=Section.objects.all(), required=False
    )

    # Add a field for selecting related sections
    related_sections = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all(), required=False
    )

    class Meta:
        model = Section
        fields = [
            "identifier",
            "type",
            "title",
            "source",
            "container",
            "reference_section",
            "insertion_method",
            "related_sections",
        ]

    def __init__(self, *args, **kwargs):
        self.section_id = kwargs.pop("section_id", None)
        self.text_id = kwargs.pop(
            "text_id", None
        )  # This will be None if not explicitly passed
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.section_id:
            logger.info('Section ID is not None')
            # Handling for updating an existing section
            section = Section.objects.get(id=self.section_id)
            self.fields["source"].initial = section.source
            self.fields["selected_tokens"].initial = ",".join(
                str(token.id) for token in section.tokens.all()
            )
            self.fields["reference_section"].initial = section.previous
            self.fields["container"].initial = section.container
            self.fields["related_sections"].initial = section.related_to.all()
        else:
            # Handling for creating a new section where text_id is necessary
            logger.info('Section ID is None')
            if self.text_id:
                text = Text.objects.get(id=self.text_id)
                section_queryset = Section.objects.filter(text=text).order_by("type")
                self.fields["container"].queryset = section_queryset
                self.fields["reference_section"].queryset = section_queryset
                self.fields["related_sections"].queryset = section_queryset
            else:
                logger.debug("Creating new section but no text_id provided")

    def save(self, commit=True):
        insertion_method = self.cleaned_data.get("insertion_method")
        reference_section = self.cleaned_data.get("reference_section")
        selected_token_ids = self.cleaned_data.get("selected_tokens").split(",")
        related_sections = self.cleaned_data.get("related_sections")

        text = (
            Text.objects.get(id=self.text_id) if self.text_id else Text.objects.first()
        )

        if self.section_id:
            # Update existing section
            new_section = Section.objects.get(id=self.section_id)
            new_section.identifier = self.cleaned_data.get("identifier")
            new_section.type = self.cleaned_data.get("type")
            new_section.title = self.cleaned_data.get("title")
            new_section.source = self.cleaned_data.get("source")
            new_section.container = self.cleaned_data.get("container")
            new_section.text = text
        else:
            # Create new section
            new_section_data = {
                "identifier": self.cleaned_data.get("identifier"),
                "type": self.cleaned_data.get("type"),
                "title": self.cleaned_data.get("title"),
                "source": self.cleaned_data.get("source"),
                "container": self.cleaned_data.get("container"),
                "text": text,
            }
            if insertion_method == "before" and reference_section:
                new_section = Section.insert_before(
                    reference_section.id, new_section_data, user=self.user
                )
            elif insertion_method == "after" and reference_section:
                new_section = Section.insert_after(
                    reference_section.id, new_section_data, user=self.user
                )
            else:
                new_section = Section(**new_section_data)

        if commit:
            new_section.save()

        if selected_token_ids:
            new_section.tokens.clear()  # Clear existing tokens before adding new ones
            for token_id in selected_token_ids:
                try:
                    token = Token.objects.get(id=token_id)
                    new_section.tokens.add(token)
                except Token.DoesNotExist:
                    logger.error(f"Token with ID {token_id} does not exist")

        # Add the related sections
        for section in related_sections:
            new_section.related_to.add(section)

        return new_section
