from django.conf import settings
from django.core.management.base import BaseCommand
from treeflow.dict.models.lemma import Lemma
from treeflow.dict.models.meaning import Meaning

class Command(BaseCommand):
    help = 'Deletes all Lemmas and Meanings objects'


    def handle(self, *args, **options):
        # Temporarily set Elasticsearch settings to False
            settings.ELASTICSEARCH_DSL_AUTOSYNC = False
            settings.ELASTICSEARCH_DSL_AUTO_REFRESH = False

            # Delete the Lemmas and Meanings objects
            Lemma.objects.all().delete()
            Meaning.objects.all().delete()

            settings.ELASTICSEARCH_DSL_AUTOSYNC = True
            settings.ELASTICSEARCH_DSL_AUTO_REFRESH = True

