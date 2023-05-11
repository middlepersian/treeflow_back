from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from treeflow.corpus.models.text import Text

class Command(BaseCommand):
    help = 'Deletes a Text object based on its identifier.'

    def add_arguments(self, parser):
        parser.add_argument('identifier', type=str, help='The identifier of the Text object to be deleted.')

    def handle(self, *args, **options):
        # Temporarily set Elasticsearch settings to False
            settings.ELASTICSEARCH_DSL_AUTOSYNC = False
            settings.ELASTICSEARCH_DSL_AUTO_REFRESH = False
            identifier = options['identifier']

            # Find the Text object with the given identifier
            text = get_object_or_404(Text, identifier=identifier)

            # Delete the Text object
            text.delete()

            self.stdout.write(self.style.SUCCESS(f"Successfully deleted Text object with identifier '{identifier}'."))

            settings.ELASTICSEARCH_DSL_AUTOSYNC = True
            settings.ELASTICSEARCH_DSL_AUTO_REFRESH = True

