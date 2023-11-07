from django.core.management.base import BaseCommand
from treeflow.dict.models.lemma import Lemma
from treeflow.dict.models.meaning import Sense


class Command(BaseCommand):
    help = 'Deletes all Lemmas and Meanings objects'

    def handle(self, *args, **options):
        # Delete the Lemmas and Meanings objects
        Lemma.objects.all().delete()
        Sense.objects.all().delete()
