import uuid as uuid_lib
from django.db import models


class DependencyManager(models.Manager):
    def get_by_natural_key(self, head, rel):
        return self.get(head=head, rel=rel)


class Dependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    head = models.ForeignKey("Token", on_delete=models.SET_NULL, related_name='dependency_head', null=True)
    rel = models.CharField(max_length=9)
    # producer values: manual(1), computational(2). see schemas/dependency_enum.py
    producer = models.SmallIntegerField(null=True, blank=True)

    objects = DependencyManager()

    def __str__(self):
        return '{} {}'.format(str(self.head), self.rel)
