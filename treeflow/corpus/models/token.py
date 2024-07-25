import uuid as uuid_lib
from typing import List

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint

import treeflow.corpus.models
from treeflow.utils.normalize import strip_and_normalize
from django.db import transaction
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

class Token(models.Model):
    NEW_NUMBER_GAP = 0.01

    id = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    number_in_sentence = models.FloatField(blank=True, null=True)

    root = models.BooleanField(default=False)
    word_token = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    text = models.ForeignKey('Text', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='text_tokens')
    image = models.ForeignKey('images.Image', on_delete=models.CASCADE,
                              null=True, blank=True, related_name='image_tokens')

    language = models.CharField(max_length=3, null=True, blank=True)
    transcription = models.CharField(max_length=50, null=True, blank=True)
    transliteration = models.CharField(max_length=50, null=True, blank=True)
    lemmas = models.ManyToManyField(
        'dict.Lemma', blank=True, through='TokenLemma', related_name='lemma_tokens')
    senses = models.ManyToManyField(
        'dict.Sense', blank=True, through='TokenSense', related_name='sense_tokens')

    avestan = models.CharField(max_length=50, null=True, blank=True)
    previous = models.OneToOneField('self',
                                     related_name='next',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL)

    gloss = models.TextField(blank=True, null=True)

    multiword_token = models.BooleanField(default=False)
    multiword_token_number = ArrayField(models.FloatField(
        blank=True, null=True), null=True, blank=True)
    related_tokens = models.ManyToManyField('self', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_tokens')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='modified_tokens',
        blank=True
    )


    class Meta:
        ordering = ['text', 'number']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'number'], name='token_text_number'
            ),
        ]
        indexes = [
            models.Index(fields=['transcription']),
            models.Index(fields=['transliteration']),
            models.Index(fields=['number']),
            models.Index(fields=['text']),
            models.Index(fields=['number', 'text', 'language', 'transcription']),
        ]

    def __str__(self):
        return '{}'.format(self.transcription)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        user = kwargs.pop('user', None)

        if self.transcription:
            self.transcription = strip_and_normalize('NFC', self.transcription)

        if self.transliteration:
            self.transliteration = strip_and_normalize('NFC', self.transliteration)

        if self.avestan:
            self.avestan = strip_and_normalize('NFC', self.avestan)

        if self.gloss:
            self.gloss = strip_and_normalize('NFC', self.gloss)

        if self.language:
            self.language = self.language.strip().lower()

        if is_new and user:
            self.created_by = user
        elif not is_new:
            self.modified_at = timezone.now()
            self.modified_by = user
            if 'update_fields' in kwargs:
                update_fields = set(kwargs['update_fields'])
                update_fields.update({'modified_at', 'modified_by'})
                kwargs['update_fields'] = list(update_fields)

        super().save(*args, **kwargs)

    @staticmethod
    def find_nearest_tokens(token_number, text_id):
        previous_token = Token.objects.filter(
            number__lt=token_number, text_id=text_id).order_by('-number').first()
        next_token = Token.objects.filter(
            number__gt=token_number, text_id=text_id).order_by('number').first()
        return previous_token, next_token

    @staticmethod
    def calculate_insert_number(before_number, after_number):
        return (before_number + after_number) / 2.0

    @classmethod
    def insert_before(cls, reference_token_id, new_token_data, user=None):
        with transaction.atomic():
            reference_token = cls.objects.select_for_update().get(id=reference_token_id)
            text_id = reference_token.text_id
            previous_token, next_token = cls.find_nearest_tokens(
                reference_token.number, text_id)
            before_number = previous_token.number if previous_token else (
                reference_token.number - cls.NEW_NUMBER_GAP)
            after_number = reference_token.number
            new_number = cls.calculate_insert_number(
                before_number, after_number)

            # Create a new token with the determined number and other data
            new_token = cls(**new_token_data)
            new_token.text_id = text_id

            # next token (reference)
            reference_token.previous = new_token
            reference_token.save()

            # unless we are at the beginning of the text
            if previous_token:
                new_token.previous = previous_token
                new_token.number = new_number
                logger.info('previous token exists')
                # log the previous token number
                logger.info('previous token number: {}'.format(previous_token.number))
            else:
                new_token.number = reference_token.number - 1
                logger.info('previous token does not exist')
                logger.info('new token number: {}'.format(new_token.number))

            new_token.save(user=user)
            return new_token

    @classmethod
    def insert_after(cls, reference_token_id, new_token_data, user=None):
        with transaction.atomic():  # Start a transaction to ensure atomicity.
            # Fetch the reference token with a lock to prevent concurrent modifications.
            reference_token = cls.objects.select_for_update().get(id=reference_token_id)

            # Find the next token based on the current position to determine proper links.
            _, next_token = cls.find_nearest_tokens(reference_token.number, reference_token.text_id)

            # Prepare and validate the new token number based on the position it should take.
            before_number = reference_token.number
            after_number = next_token.number if next_token else (before_number + cls.NEW_NUMBER_GAP)
            new_number = cls.calculate_insert_number(before_number, after_number)

            # Create the new token with the proper number and additional data provided.
            new_token = cls.objects.create(text_id=reference_token.text_id, **new_token_data)

            # If we are not at the end of the text, update the 'previous' field of the next token to point to the new token.
            if next_token:
                next_token.previous = new_token
                next_token.save()
                logger.info('next token exists')
                # add the number of the new token
                new_token.number = new_number
                logger.info('new token number: {}'.format(new_number))

            else:
                logger.info('next token does not exist')
                new_token.number = reference_token.number + 1
                logger.info('new token number: {}'.format(reference_token.number + 1))

            # Update the 'next' field of the reference token to point to the new token.
            new_token.previous = reference_token
            new_token.save(user=user)

            return new_token

    @classmethod
    def delete_token(cls, token_id):
        with transaction.atomic():
            # Retrieve the token to delete and lock the row
            token_to_delete = cls.objects.select_for_update().get(id=token_id)

            # Retrieve the related previous and next tokens if they exist
            previous_token = token_to_delete.previous
            next_token = Token.objects.filter(previous=token_to_delete).first()

            # clear up current previous from current token
            token_to_delete.previous = None
            token_to_delete.save()

            # Update the next token to point to the previous token
            if next_token:
                next_token.previous = previous_token  # This could set it to None if previous_token doesn't exist
                next_token.save()

            # Now delete the token
            token_to_delete.delete()

    def sentence(self) -> 'treeflow.corpus.models.Section':
        return treeflow.corpus.models.Section.objects.get(type='sentence', tokens=self)


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
            models.Index(fields=['sense']),
        ]
