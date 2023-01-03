import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from .comment import Comment
from .token import Token

class TokenComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    uncertain = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    to_discuss = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    new_suggestion = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    
