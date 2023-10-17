from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from treeflow.corpus.models.text import Text


class Command(BaseCommand):
    help = 'Deletes a Text object based on its identifier.'

    def add_arguments(self, parser):
        parser.add_argument(
            'identifier', type=str, help='The identifier of the Text object to be deleted.')

    def handle(self, *args, **options):

        identifier = options['identifier']

        # Find the Text object with the given identifier
        text = get_object_or_404(Text, identifier=identifier)

        # Delete the Text object
        text.delete()
