from django.conf import settings
from django.core.management.base import BaseCommand
from treeflow.corpus.models.text import Text

class Command(BaseCommand):
    help = 'Deletes a Text object based on its title.'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='The title of the Text object to be deleted.')

    def handle(self, *args, **options):



        settings.ELASTICSEARCH_DSL_AUTOSYNC = False
        settings.ELASTICSEARCH_DSL_AUTO_REFRESH = False

        title = options['title']

        # Find the Text object with the given title
        try:
            text = Text.objects.get(title=title)
        except Text.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Error: Text object with title '{title}' not found."))
            return

        # Delete the Text object
        text.delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted Text object with title '{title}'."))
        settings.ELASTICSEARCH_DSL_AUTOSYNC = True
        settings.ELASTICSEARCH_DSL_AUTO_REFRESH = True
