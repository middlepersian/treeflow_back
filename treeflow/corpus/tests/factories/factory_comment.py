import factory
from treeflow.corpus.models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory("treeflow.corpus.tests.factories.UserFactory")
    txt = factory.Faker("text")

    dependency = factory.SubFactory("treeflow.corpus.tests.factories.DependencyFactory")
    image = factory.SubFactory("treeflow.images.tests.factories.ImageFactory")
    source = factory.SubFactory("treeflow.corpus.tests.factories.SourceFactory")
    section_type = factory.SubFactory("treeflow.corpus.tests.factories.SectionTypeFactory")
    section = factory.SubFactory("treeflow.corpus.tests.factories.SectionFactory")
    text = factory.SubFactory("treeflow.corpus.tests.factories.TextFactory")

    token = factory.SubFactory("treeflow.corpus.tests.factories.TokenFactory")
    uncertain = factory.List(["a", "b", "c"])
    to_discuss = factory.List(["d", "e", "f"])
    new_suggestion = factory.List(["g", "h", "i"])
