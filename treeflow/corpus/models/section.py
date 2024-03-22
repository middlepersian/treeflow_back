from django.db import models
from django.conf import settings
from django.db import transaction
from django.utils import timezone
import uuid as uuid_lib
from treeflow.utils.normalize import strip_and_normalize

import logging

logger = logging.getLogger(__name__)

class Section(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey('Text', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='section_text')
    number = models.FloatField(null=True, blank=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=3, blank=True, null=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL,
                               related_name='section_source', null=True, blank=True)
    tokens = models.ManyToManyField('Token', related_name='section_tokens', through='SectionToken')
    previous = models.OneToOneField('self', on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='next')
    # this is the case if a section "paragraph" has a "chapter" container
    container = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='section_container')
    # graph structure for related sections
    related_to = models.ManyToManyField('self', related_name='section_related_to')

    senses = models.ManyToManyField(
        'dict.Sense', related_name='section_senses')


    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_sections')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_sections',
        blank=True
    )

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'identifier'], name='section_text_identifier')
        ]
        indexes = [models.Index(fields=['identifier']),
                   models.Index(fields=['type']),
                   models.Index(fields=['number']),
                   models.Index(fields=['type', 'text']),]

    def __str__(self) -> str:
        return '{} - {} '.format(self.type, self.identifier)

    @property
    def has_Enhanced(self) -> bool:
        return self.tokens.filter(dependency_token__enhanced=True).exists()

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.identifier:
            # normalize identifier
            self.identifier = strip_and_normalize('NFC', self.identifier)
        if self.type:
            # normalize type
            self.type = strip_and_normalize('NFC', self.type)
        if self.title:
            # process title
            self.title = strip_and_normalize('NFC', self.title)
        if self.language:
            # process language
            self.language = self.language.strip().lower()
        
        is_new = self._state.adding
        logger.debug(f"Section.save: is_new={is_new}")
        user = kwargs.pop('user', None)
        # Handle the user for created_by and modified_by
        if is_new and user:
            self.created_by = user
        elif not is_new:
            self.modified_at = timezone.now()
            self.modified_by = user

            # Ensure 'modified_at' and 'modified_by' are included in 'update_fields'
            if 'update_fields' in kwargs:
                update_fields = set(kwargs['update_fields'])
                update_fields.update({'modified_at', 'modified_by'})
                kwargs['update_fields'] = list(update_fields)

        super().save(*args, **kwargs)

    @classmethod
    def find_adjacent_sections(cls, reference_section_id):
        reference_section = cls.objects.get(id=reference_section_id)

        # Find the previous section
        previous_section = reference_section.previous

        # Find the next section by searching for a section that has the current section as its previous
        next_section = cls.objects.filter(previous_id=reference_section_id).first()

        return previous_section, next_section

    @classmethod
    def calculate_dynamic_gap(cls, reference_section_id):
        # Fetch the reference, previous, and next sections
        reference_section = cls.objects.get(id=reference_section_id)
        previous_section, next_section = cls.find_adjacent_sections(reference_section_id)

        # Set a default minimum gap
        default_min_gap = 0.1  # Adjust this value as needed

        # If both previous and next sections are available
        if previous_section and next_section and previous_section.number is not None and next_section.number is not None:
            gap_before = reference_section.number - previous_section.number
            gap_after = next_section.number - reference_section.number
            return min(gap_before, gap_after) / 2.0  # Average of the smaller gap

        # If only previous section is available
        elif previous_section and previous_section.number is not None:
            gap_before = reference_section.number - previous_section.number
            return gap_before / 2.0

        # If only next section is available
        elif next_section and next_section.number is not None:
            gap_after = next_section.number - reference_section.number
            return gap_after / 2.0

        # Fallback to a default minimum gap
        return default_min_gap

    @classmethod
    def insert_before(cls, reference_section_id, new_section_data):
        with transaction.atomic():
            reference_section = cls.objects.select_for_update().get(id=reference_section_id)
            previous_section, _ = cls.find_adjacent_sections(reference_section_id)

            # Create the new section
            new_section = cls(**new_section_data)

            # Calculate the dynamic gap
            dynamic_gap = cls.calculate_dynamic_gap(reference_section_id)

            # Calculate the number for the new section
            if previous_section and previous_section.number is not None:
                # Calculate the number by using the dynamic gap
                new_section.number = previous_section.number + dynamic_gap
            elif reference_section.number is not None:
                # Use the reference section's number minus the dynamic gap
                new_section.number = reference_section.number - dynamic_gap
            else:
                # If the reference section doesn't have a number, set to None or a default value
                new_section.number = None

            # update the reference section's previous link
            reference_section.previous = new_section
            reference_section.save()

            if previous_section:
                # Link the new section with the previous section
                new_section.previous = previous_section

            # Save the new section
            new_section.save()

            return new_section

    @classmethod
    def insert_after(cls, reference_section_id, new_section_data):
        with transaction.atomic():
            reference_section = cls.objects.select_for_update().get(id=reference_section_id)
            _, next_section = cls.find_adjacent_sections(reference_section_id)

            # Create the new section
            new_section = cls(**new_section_data)

            # Calculate the dynamic gap
            dynamic_gap = cls.calculate_dynamic_gap(reference_section_id)

            # Calculate the number for the new section
            if next_section and next_section.number is not None:
                # Calculate the number by using the dynamic gap
                new_section.number = reference_section.number + dynamic_gap
            elif reference_section.number is not None:
                # Use the reference section's number plus the dynamic gap
                new_section.number = reference_section.number + dynamic_gap
            else:
                # If the reference section doesn't have a number, set to None or a default value
                new_section.number = None

            if next_section:
                # Link the new section with the next section
                next_section.previous = new_section
                next_section.save()

            # Link the new section with the reference section
            new_section.previous = reference_section
            new_section.save()

            return new_section


class SectionToken(models.Model):
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    token = models.ForeignKey('Token', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['section', 'token']),
            models.Index(fields=['token']),
            models.Index(fields=['section']),
        ]
        ordering = ['section', 'token']

    def __str__(self):
        return 'SectionToken {}:{}'.format(self.section_id, self.token_id)
