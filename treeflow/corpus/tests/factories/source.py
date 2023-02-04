import factory
from treeflow.corpus.models import Source

class SourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Source

    type = factory.Faker("pystr", min_chars=1, max_chars=10)     

    identifier = factory.Faker("pystr", min_chars=1, max_chars=15)
    references = factory.RelatedFactory("treeflow.corpus.tests.factories.BibEntryFactory")
    description = factory.Faker("text")

    @factory.post_generation
    def sources(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for source in extracted:
                self.sources.add(source)
