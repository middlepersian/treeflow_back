import factory
from treeflow.corpus.models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory("treeflow.corpus.tests.factories.UserFactory")
    txt = factory.Faker("text")

    codex = factory.SubFactory("treeflow.corpus.tests.factories.CodexFactory")
    dependency = factory.SubFactory("treeflow.corpus.tests.factories.DependencyFactory")
    edition = factory.SubFactory("treeflow.corpus.tests.factories.EditionFactory")
    facsimile = factory.SubFactory("treeflow.corpus.tests.factories.FacsimileFactory")
    folio = factory.SubFactory("treeflow.corpus.tests.factories.FolioFactory")
    line = factory.SubFactory("treeflow.corpus.tests.factories.LineFactory")
    resource = factory.SubFactory("treeflow.corpus.tests.factories.ResourceFactory")
    section_type = factory.SubFactory("treeflow.corpus.tests.factories.SectionTypeFactory")
    section = factory.SubFactory("treeflow.corpus.tests.factories.SectionFactory")
    sentence = factory.SubFactory("treeflow.corpus.tests.factories.SentenceFactory")
    text_sigle = factory.SubFactory("treeflow.corpus.tests.factories.TextSigleFactory")
    text = factory.SubFactory("treeflow.corpus.tests.factories.TextFactory")

    token = factory.SubFactory("treeflow.corpus.tests.factories.TokenFactory")
    uncertain = factory.List(["a", "b", "c"])
    to_discuss = factory.List(["d", "e", "f"])
    new_suggestion = factory.List(["g", "h", "i"])
