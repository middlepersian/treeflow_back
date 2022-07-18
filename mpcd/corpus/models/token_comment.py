import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings

from .comment import Comment
from .comment_category import CommentCategory


class TokenComment(Comment):
    uncertain = models.ManyToManyField(CommentCategory, blank=True, related_name='token_comment_uncertain')
    to_discuss = models.ManyToManyField(CommentCategory, blank=True, related_name='token_comment_to_discuss')
    new_suggestion = models.ManyToManyField(CommentCategory, blank=True, related_name='token_comment_new_suggestion')
