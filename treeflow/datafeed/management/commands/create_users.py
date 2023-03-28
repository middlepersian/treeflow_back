from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from treeflow.users.models import User

class Command(BaseCommand):
    help = 'Creates users from a text file and assigns them the "editor" role.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The path to the text file with usernames and passwords.')

    def handle(self, *args, **options):
        filename = options['filename']

        # Try to get the "editor" group or create it if it doesn't exist
        try:
            group = Group.objects.get(name='editor')
        except Group.DoesNotExist:
            group = Group.objects.create(name='editor')

        # Open the text file and read the usernames and passwords
        with open(filename) as f:
            for line in f:
                # Strip leading/trailing whitespace and split on tab
                fields = line.strip().split('\t')

                # Check for empty username
                if not fields[0]:
                    self.stdout.write(self.style.ERROR('Error: Empty username.'))
                    continue

                # Check if user already exists
                try:
                    user = User.objects.get(username=fields[0])
                    created = False
                except User.DoesNotExist:
                    user = User.objects.create_user(username=fields[0], password=fields[1])
                    created = True

                # Set staff status
                user.is_staff = True
                #save
                user.save()

                # Assign the "editor" role to the user
                user.groups.add(group)

                # Log success message
                self.stdout.write(self.style.SUCCESS(f'Successfully {"created" if created else "updated"} user "{user.username}" and assigned the "editor" role.'))
