import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from .comment import Comment


class TokenComment(Comment):
    uncertain = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    to_discuss = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    new_suggestion = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    
