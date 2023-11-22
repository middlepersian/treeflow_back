from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize
from django.db import transaction


class Section(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey('Text', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='section_text')
    number = models.FloatField(null=True, blank=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=3, blank=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL,
                               related_name='section_source', null=True, blank=True)
    tokens = models.ManyToManyField('Token', related_name='section_tokens', through='SectionToken')
    previous = models.OneToOneField('self', on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='next')
    # this is the case if a section "paragraph" has a "chapter" container
    container = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='section_container')

    senses = models.ManyToManyField(
        'dict.Sense', related_name='section_senses')

    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'identifier'], name='section_text_identifier')
        ]
        indexes = [models.Index(fields=['text', 'type']),
                   models.Index(fields=['type']),
                   ]

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
        super().save(*args, **kwargs)

    MIN_GAP = 0.01  # Define a class-level constant for the minimum gap

    @staticmethod
    def find_adjacent_sections(section_number, text_id):
        previous_section = Section.objects.filter(
            number__lt=section_number, text_id=text_id).order_by('-number').first()
        next_section = Section.objects.filter(
            number__gt=section_number, text_id=text_id).order_by('number').first()
        return previous_section, next_section

    @staticmethod
    def calculate_insert_number(before_number, after_number):
        return (before_number + after_number) / 2.0

    MIN_GAP = 0.01  # Define a class-level constant for the minimum gap

    @staticmethod
    def calculate_insert_number(before_number, after_number):
        # Assuming we have a standard gap we observe, e.g., 0.1
        # The logic here finds the midway point between two numbers,
        # but you could implement a different logic that suits your needs.
        return (before_number + after_number) / 2.0


    @classmethod
    def insert_before(cls, reference_section_id, new_section_data):
        with transaction.atomic():
            reference_section = cls.objects.select_for_update().get(id=reference_section_id)
            text_id = reference_section.text_id
            previous_section, _ = cls.find_adjacent_sections(reference_section.number, text_id)

            before_number = previous_section.number if previous_section else (reference_section.number - cls.MIN_GAP)
            after_number = reference_section.number
            new_number = cls.calculate_insert_number(before_number, after_number)

            new_section = cls(number=new_number, text_id=text_id, **new_section_data)
            new_section.text_id = text_id

            # next section is the reference section
            reference_section.previous = new_section
            reference_section.save()

            #unless we are at the beginning of the list
            if previous_section:
                new_section.previous = previous_section
            new_section.save()
            return new_section

    @classmethod
    def insert_after(cls, reference_section_id, new_section_data):
        with transaction.atomic():
            reference_section = cls.objects.select_for_update().get(id=reference_section_id)
            text_id = reference_section.text_id
            _, next_section = cls.find_adjacent_sections(reference_section.number, text_id)

            before_number = reference_section.number
            after_number = next_section.number if next_section else (before_number + cls.MIN_GAP)
            new_number = cls.calculate_insert_number(before_number, after_number)

            new_section = cls(number=new_number, text_id=text_id, **new_section_data)

            # if we are not at the ned of the list, update the previous section
            if next_section:
                next_section.previous = new_section
                next_section.save()

            # update the next field of the reference section
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
