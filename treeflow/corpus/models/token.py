import uuid as uuid_lib
from django.db import models
from django.db.models import Q, F
from django.db.models import Q, F
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize
from django.db import transaction

class Token(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    number_in_sentence = models.FloatField(blank=True, null=True)

    root = models.BooleanField(default=False)
    word_token = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    text = models.ForeignKey('Text', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='token_text')
    image = models.ForeignKey('images.Image', on_delete=models.CASCADE,
                              null=True, blank=True, related_name='token_image')

    language = models.CharField(max_length=3, null=True, blank=True)
    transcription = models.TextField(null=True, blank=True)
    transliteration = models.TextField(null=True, blank=True)
    lemmas = models.ManyToManyField(
        'dict.Lemma', blank=True, through='TokenLemma', related_name='token_lemmas')
    senses = models.ManyToManyField(
        'dict.Sense', blank=True, through='TokenSense', related_name='token_senses')

    avestan = models.TextField(null=True, blank=True)

    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL, db_index=True)

    gloss = models.TextField(blank=True, null=True)

    multiword_token = models.BooleanField(default=False)
    multiword_token_number = ArrayField(models.FloatField(
        blank=True, null=True), null=True, blank=True)
    related_tokens = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'number'], name='token_text_number'
            )
        ]
        indexes = [
            models.Index(fields=['transcription']),
            models.Index(fields=['transliteration']),
            models.Index(fields=['number']),
        ]

    def __str__(self):
        return '{}'.format(self.transcription)

    def save(self, *args, **kwargs):
        # normalize transcription
        if self.transcription:
            self.transcription = strip_and_normalize('NFC', self.transcription)

        # normalize transliteration
        if self.transliteration:
            self.transliteration = strip_and_normalize(
                'NFC', self.transliteration)

        # normalize language
        if self.language:
            # lowercase
            self.language = self.language.strip().lower()

        # normalize avestan
        if self.avestan:
            self.avestan = strip_and_normalize('NFC', self.avestan)

        # normalize gloss
        if self.gloss:
            self.gloss = strip_and_normalize('NFC', self.gloss)

        # save
        super().save(*args, **kwargs)

    MIN_GAP = 0.01  # Define a class-level constant for the minimum gap    

    @staticmethod
    def find_nearest_tokens(token_number, text_id):
        previous_token = Token.objects.filter(number__lt=token_number, text_id=text_id).order_by('-number').first()
        next_token = Token.objects.filter(number__gt=token_number, text_id=text_id).order_by('number').first()
        return previous_token, next_token

    @staticmethod
    def calculate_insert_number(before_number, after_number):
        # Assuming we have a standard gap we observe, e.g., 0.1
        # The logic here finds the midway point between two numbers,
        # but you could implement a different logic that suits your needs.
        return (before_number + after_number) / 2.0

    @classmethod
    def insert_before(cls, reference_token_id, new_token_data):
        with transaction.atomic():
            reference_token = cls.objects.select_for_update().get(id=reference_token_id)
            text_id = reference_token.text_id
            previous_token, next_token = cls.find_nearest_tokens(reference_token.number, text_id)
            before_number = previous_token.number if previous_token else (reference_token.number - cls.MIN_GAP)
            after_number = reference_token.number
            new_number = cls.calculate_insert_number(before_number, after_number)

            # Create a new token with the determined number and other data
            new_token = cls(number=new_number, **new_token_data)
            new_token.text_id = text_id
            new_token.save()

            # Update the 'next' field of the previous token to point to the new token, if applicable
            if previous_token:
                previous_token.next = new_token
                previous_token.save()

            # Update the 'previous' field of the reference token to point to the new token
            reference_token.previous = new_token
            reference_token.save()

            # Update the 'next' field of the new token to point to the reference token
            new_token.next = reference_token
            new_token.save()

            # Update the 'previous' field of the next token to point to the new token, if applicable
            if next_token and not next_token.previous_id:
                next_token.previous = new_token
                next_token.save()

            return new_token
            
    @classmethod
    def insert_after(cls, reference_token_id, new_token_data):
        with transaction.atomic():
            reference_token = cls.objects.select_for_update().get(id=reference_token_id)
            text_id = reference_token.text_id
            _, next_token = cls.find_nearest_tokens(reference_token.number, text_id)
            before_number = reference_token.number
            after_number = next_token.number if next_token else (reference_token.number + cls.MIN_GAP)
            new_number = cls.calculate_insert_number(before_number, after_number)

            # Create a new token with the determined number and other data
            new_token = cls(number=new_number, **new_token_data)
            new_token.text_id = text_id
            new_token.save()

            # Update the 'previous' field of the new token to point to the reference token
            if not cls.objects.filter(previous=reference_token).exists():
                new_token.previous = reference_token
                new_token.save()

            # Update the 'next' field of the reference token to point to the new token
            if reference_token and not reference_token.next:
                reference_token.next = new_token
                reference_token.save()
                print(f"After updating reference_token.next: {reference_token.next}")
                
            # Update the 'previous' field of the next token to point to the new token, if applicable
            if next_token and not cls.objects.filter(previous=new_token).exists():
                next_token.previous = new_token
                next_token.save()

            # Update the 'next' field of the new token to point to the next token, if applicable
            if next_token and not new_token.next:
                new_token.next = next_token
                new_token.save()

            return new_token
class TokenLemma(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    lemma = models.ForeignKey('dict.Lemma', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['token', 'lemma']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['lemma']),
        ]


class TokenSense(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    sense = models.ForeignKey('dict.Sense', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['token', 'sense']
        indexes = [
            models.Index(fields=['token']),
        ]
