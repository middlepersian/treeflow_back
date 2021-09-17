import uuid as uuid_lib
from django.db import models


class AuthorManager(models.Manager):
    def get_by_natural_key(self, name, last_name):
        return self.get(name=name, last_name=last_name)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)

    objects = AuthorManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'last_name'], name='name_lastname'
            )
        ]
