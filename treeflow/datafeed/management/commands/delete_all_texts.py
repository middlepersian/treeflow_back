from django.conf import settings
from django.core.management.base import BaseCommand
from treeflow.corpus.models.text import Text

class Command(BaseCommand):
    help = 'Deletes all Texts'


    def handle(self, *args, **options):
        # Temporarily set Elasticsearch settings to False
            settings.ELASTICSEARCH_DSL_AUTOSYNC = False
            settings.ELASTICSEARCH_DSL_AUTO_REFRESH = False

            # Delete the Lemmas and Meanings objects
            Text.objects.all().delete()

            settings.ELASTICSEARCH_DSL_AUTOSYNC = True
            settings.ELASTICSEARCH_DSL_AUTO_REFRESH = True

