import factory
from mpcd.corpus.models import Text
from mpcd.corpus.tests.factories.corpus import CorpusFactory
from mpcd.corpus.tests.factories.text_sigle import TextSigleFactory
from mpcd.corpus.tests.factories.source import SourceFactory
from mpcd.corpus.tests.factories.bibliography import BibEntryFactory
from mpcd.users.tests.factories import UserFactory

class TextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Text
    corpus = factory.SubFactory(CorpusFactory)
    title = factory.Faker("pystr", min_chars=1, max_chars=30)
    text_sigle = factory.SubFactory(TextSigleFactory)
    stage = factory.Faker("pystr", max_chars=3  )

    @factory.post_generation
    def editors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for editor in extracted:
                self.editors.add(editor)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)

    @factory.post_generation
    def collaborators(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for collaborator in extracted:
                self.collaborators.add(collaborator)

    @factory.post_generation
    def sources(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for source in extracted:
                self.sources.add(source)

    @factory.post_generation
    def resources(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for resource in extracted:
                self.resources.add(resource)
               
               
            
             