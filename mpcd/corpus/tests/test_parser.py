from django.test import TestCase
import pytest
import factory
from faker import Faker
from mpcd.corpus.models import Codex, CodexPart, Facsimile, Folio, Line, BibEntry, MorphologicalAnnotation, Token


class CodexFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Codex

    sigle = factory.Faker("pystr",  max_chars=5)


class CodexPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CodexPart

    slug = factory.Faker("slug")
    codex = factory.SubFactory(CodexFactory)


class BibEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BibEntry

    key = factory.Faker("pystr",  max_chars=5)


class FacsimileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facsimile

    bib_entry = factory.SubFactory(BibEntryFactory)
    codex_part = factory.SubFactory(CodexPartFactory)

###


class CorpusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corpus

    name = factory.Faker("pystr", max_chars=10)
    slug = factory.Faker("pystr", max_chars=10)


class TextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Text

    id = factory.Faker("uuid4")
    corpus = factory.SubFactory("path.to.CorpusFactory")
    title = factory.Faker("sentence", nb_words=4)
    text_sigle = factory.SubFactory("path.to.TextSigleFactory")
    stage = factory.Faker("pystr", max_chars=3)


class MorphologicalAnnotationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MorphologicalAnnotation

    feature = factory.Faker("pystr", max_chars=10)
    feature_value = factory.Faker("pystr", max_chars=10)


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    number = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    root = factory.Faker("pybool")
    word_token = factory.Faker("pybool")
    visible = factory.Faker("pybool")
    text = factory.SubFactory("your_app.factories.TextFactory")
    language = factory.Faker("language_code")
    transcription = factory.Faker("word")
    transliteration = factory.Faker("word")
    lemmas = factory.SubFactory("your_app.factories.LemmaFactory")
    meanings = factory.SubFactory("your_app.factories.MeaningFactory")
    pos = factory.Faker("word", length=8)
    morphological_annotation = factory.SubFactory("your_app.factories.MorphologicalAnnotationFactory")
    syntactic_annotation = factory.SubFactory("your_app.factories.DependencyFactory")
    comments = factory.SubFactory("your_app.factories.TokenCommentFactory")
    avestan = factory.Faker("text")
    line = factory.SubFactory(L)
    previous = factory.SubFactory("self")
    gloss = factory.Faker("text")


@pytest.mark.django_db
def test_create_facsimile():
    # Create a Codex object
    codex = CodexFactory()

    # Create a CodexPart object
    codex_part = CodexPartFactory(codex=codex)

    # Create a BibEntry object
    bib_entry = BibEntryFactory()

    # Create a Facsimile object
    facsimile = FacsimileFactory(codex_part=codex_part, bib_entry=bib_entry)

    # Assert that the Facsimile object was created correctly
    assert facsimile.codex_part == codex_part
    assert facsimile.bib_entry == bib_entry


def parse_sentences(sentences, facsimile,  line_identifiers, folio_identifiers, text):
    # Assume that the list is called 'sentences'
    line_count = {}
    folio_count = {}
    previous_folio_obj = None  # Initialize the previous_folio_obj variable
    previous_line_obj = None  # Initialize the previous_line_obj variable
    previous_token_obj = None  # Initialize the previous_token_obj variable
    previous_sentence_obj = None  # Initialize the previous_sentence_obj variable
    for sentence in sentences:
        for token_dict in sentence['tokens']:
            line_identifier = str(token_dict['folio']) + '_' + \
                str(token_dict['line'])  # Initialize the line_id variable
            folio_identifier = facsimile.bib_entry.key + '_' + \
                str(token_dict['folio'])  # Initialize the folio_id variable

            line_identifiers.add(line_identifier)
            folio_identifiers.add(folio_identifier)

            if line_identifier not in line_count:
                line_count[line_identifier] = 1
            else:
                line_count[line_identifier] += 1
            if folio_identifier not in folio_count:
                folio_count[folio_identifier] = 1
            else:
                folio_count[folio_identifier] += 1

            # Get or create a Folio object with the specified folio ID
            folio_obj, created = Folio.objects.get_or_create(identifier=folio_identifier)
            if not created:
                # Check if this is the first time the folio has been encountered
                if folio_identifier in folio_count and folio_count[folio_identifier] > 1:
                    # Set the previous_folio field to the previous Folio object
                    folio_obj.previous_folio = previous_folio_obj
                previous_folio_obj = folio_obj  # Update the previous Folio object
                folio_obj.save()

             # Get or create a Line object with the specified line ID
            line_obj, created = Line.objects.get_or_create(identifier=line_identifier, folio=folio_obj)
            if not created:
                # Check if this is the first time the line has been encountered
                if line_identifier in line_count and line_count[line_identifier] > 1:
                    # Set the previous_line field to the previous Line object
                    line_obj.previous_line = previous_line_obj
                previous_line_obj = line_obj  # Update the previous Line object
                line_obj.save()

            # Create a Token object
            token = TokenFactory(text=text, line=line_obj, previous=previous_token_obj)
            previous_token_obj = token

            # Create a Sentence object
            sentence_obj = SentenceFactory(text=text, line=line_obj, previous=previous_sentence_obj)
            previous_sentence_obj = sentence_obj

    print(f"Number of lines: {len(line_count)}")
    print(f"Number of folios: {len(folio_count)}")

    return line_identifiers, folio_identifiers


fake = Faker()


@pytest.fixture
def sentences():
    return [
        {
            'tokens': [
                {'line': fake.pyint(), 'folio': fake.pyint()},
                {'line': fake.pyint(), 'folio': fake.pyint()},
            ]
        },
        {
            'tokens': [
                {'line': fake.pyint(), 'folio': fake.pyint()},
            ]
        },
    ]

# test_parse_sentences.py


@pytest.mark.django_db
def test_parse_sentences(sentences):
    # Call the parse_sentences function with the fake sentences
    facsimile = FacsimileFactory()
    line_identifiers = set()
    folio_identifiers = set()
    parse_sentences(sentences, facsimile=facsimile, line_identifiers=line_identifiers,
                    folio_identifiers=folio_identifiers)

    # Assert that the correct number of lines and folios were created
    assert Line.objects.count() == len(line_identifiers)
    assert Folio.objects.count() == len(folio_identifiers)
