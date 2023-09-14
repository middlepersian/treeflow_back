from django.core.management.base import BaseCommand
from treeflow.corpus.models import Source
from treeflow.images.models import Image

class Command(BaseCommand):
    help = 'Updates the source field of Image models based on their identifier'

    def handle(self, *args, **options):
        # Step 1: Iterate through all Image objects with null source
        images_without_source = Image.objects.filter(source__isnull=True)

        for img in images_without_source:
            # Step 2: Extract the sourceid from the image identifier
            source_id = img.identifier.split('_')[0]

            # Step 3: Find the corresponding Source object
            try:
                source = Source.objects.get(identifier=source_id)
            except Source.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Source with identifier {source_id} does not exist.'))
                continue

            # Step 4: Update the source field of the Image object
            img.source = source
            img.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated source for image {img.id}'))
