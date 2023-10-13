from django.core.management.base import BaseCommand


#this is the command that will be run to clear the cache
class Command(BaseCommand):
    help = 'Clears the cache.'

    def handle(self, *args, **options):
        from django.core.cache import cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Cache cleared.'))