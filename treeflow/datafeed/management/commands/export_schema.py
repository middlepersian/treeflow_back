from django.core.management import BaseCommand
from strawberry.printer import print_schema

from treeflow.schema import schema    # import your schema here

class Command(BaseCommand):
    help = 'Exports the strawberry graphql schema'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output', type=str, help='Output file path', default='schema.graphql')

    def handle(self, *args, **options):
        schema_str = print_schema(schema)
        with open(options['output'], 'w') as f:
            f.write(schema_str)
        self.stdout.write(f'Schema saved to {options["output"]}')
