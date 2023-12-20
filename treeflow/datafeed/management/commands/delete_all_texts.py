from django.core.management.base import BaseCommand
from treeflow.corpus.models.text import Text

class Command(BaseCommand):
    help = 'Deletes all Texts'


    def handle(self, *args, **options):

            # Delete the Lemmas and Meanings objects
            Text.objects.all().delete()


