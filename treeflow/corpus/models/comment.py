import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from treeflow.utils.normalize import strip_and_normalize

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    comment = models.TextField(null=True, blank=True)


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='comment_user')
    
    # dependency
    dependency = models.ForeignKey('Dependency', on_delete=models.CASCADE, null=True,
                                   blank=True, related_name='comment_dependency')

    # image
    image = models.ForeignKey('images.Image', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_image')


    # section
    section = models.ForeignKey('Section', on_delete=models.CASCADE, null=True,
                                blank=True, related_name='comment_section')

    # source
    source = models.ForeignKey('Source', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_source')                           


    # token
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_token')

    # text
    text = models.ForeignKey('Text', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_text')

    # fields for Token
    uncertain = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    to_discuss = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)
    new_suggestion = ArrayField(models.CharField(max_length=1, blank=True, null=True), blank=True, null=True)

    # lemma
    lemma = models.ForeignKey('dict.Lemma', on_delete=models.CASCADE, null=True,
                              blank=True, related_name='comment_lemma')
    #sense
    sense = models.ForeignKey('dict.Sense', on_delete=models.CASCADE, null=True,
                              blank=True, related_name='comment_sense')                            

    # semantic
    semantic = models.ForeignKey('dict.Semantic', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_comments')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_comments',
        blank=True
    )


    def __str__(self):
        return '{} {}'.format(self.user, self.comment)

    class Meta:
        pass
    
    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.comment:
            self.comment = strip_and_normalize('NFC', self.comment)

        is_new = self._state.adding
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