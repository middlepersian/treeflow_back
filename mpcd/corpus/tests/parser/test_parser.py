import os
import json
import pytest
from faker import Faker
from mpcd.corpus.models import Folio


from mpcd.corpus.tests.factories.codex import CodexFactory
from mpcd.corpus.tests.factories.codex_part import CodexPartFactory
from mpcd.corpus.tests.factories.facsimile import FacsimileFactory
from mpcd.corpus.tests.factories.bibliography import BibEntryFactory
from mpcd.corpus.tests.factories.token import TokenFactory
from mpcd.corpus.tests.factories.folio import FolioFactory
from mpcd.corpus.tests.factories.text import TextFactory
from mpcd.corpus.tests.factories.section import SectionFactory
from mpcd.corpus.tests.factories.text_sigle import TextSigleFactory
from mpcd.corpus.tests.factories.corpus import CorpusFactory
from mpcd.corpus.tests.factories.section_type import SectionTypeFactory

# models
from mpcd.corpus.models import Text
from mpcd.corpus.models import Corpus
from mpcd.corpus.models import TextSigle
from mpcd.corpus.models import Section
from mpcd.corpus.models import Codex
from mpcd.corpus.models import CodexPart
from mpcd.corpus.models import Facsimile
from mpcd.corpus.models import Folio
from mpcd.corpus.models import Token


from mpcd.corpus.tests.parser.parse_sentence import get_sentences, format_sentences


def serialize_first_elements(sentences, number_of_elements):
    file = 'sentences_{}.json'.format(number_of_elements)
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    jsonFile = open(file_path, "w")
    jsonFile.write(json.dumps(sentences[:number_of_elements], indent=4, ensure_ascii=False))


@pytest.mark.django_db
def test_create_codex():
    # Create a Codex object
    codex = CodexFactory()

    # Assert that the Codex object was created correctly
    assert codex.sigle == codex.sigle


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
    # assert facsimile.codex_part == codex_part
    # assert facsimile.bib_entry == bib_entry

    assert facsimile.codex_part.codex == codex


@pytest.mark.django_db
def test_read_file():
    file = 'GA_K20.xlsx'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)

    sentences = get_sentences(file_path)
    assert len(sentences) == 119

    sentences = format_sentences(sentences)
    assert len(sentences) == 119
    # serialize
    serialize_first_elements(sentences, 10)


@pytest.mark.django_db
def test_parse(sentences):
    # CREATE TEXT
    test_create_text()

    # get the text
    text = Text.objects.get(text_sigle__sigle="GA")
    assert text.corpus.slug == "mpcd"
    assert text.title == "Mādīgān ī Gizistag Abālīš"

    # get the facsimile
    facsimile = Facsimile.objects.get(bib_entry__key="zotero_k20")
    assert facsimile.bib_entry.key == "zotero_k20"

    line_identifiers = set()
    folio_identifiers = set()

    line_identifiers, folio_identifiers = parse_sentences(
        sentences, facsimile, line_identifiers, folio_identifiers, text)
    assert len(line_identifiers) == 119
    assert len(folio_identifiers) == 1


@pytest.mark.django_db
def test_create_text():
    # CREATE TEXT
    codex_part = CodexPartFactory(codex__sigle="K20")
    facsimile = FacsimileFactory(bib_entry__key="zotero_k20", codex_part__codex__sigle="K20", codex_part__slug="k20new")
    text = TextFactory(title="Mādīgān ī Gizistag Abālīš", text_sigle__sigle="GA", corpus__slug="mpcd")
    assert text.title == "Mādīgān ī Gizistag Abālīš"
    assert text.text_sigle.sigle == "GA"
    assert text.corpus.slug == "mpcd"


@pytest.mark.django_db
def parse_sentences(sentences, facsimile,  line_identifiers, folio_identifiers, text):

    line_count = {}
    folio_count = {}
    previous_folio_obj = None  # Initialize the previous_folio_obj variable
    previous_line_obj = None  # Initialize the previous_line_obj variable
    previous_token_obj = None  # Initialize the previous_token_obj variable
    previous_sentence_obj = None  # Initialize the previous_sentence_obj variable

    # initialize sections
    # sentence section
    sentence_section_type = SectionTypeFactory(identifier="sentence")
    # line section
    line_section_type = SectionTypeFactory(identifier="line")
    # chapter section
    chapter_section_type = SectionTypeFactory(identifier="chapter")
    # section
    section_section_type = SectionTypeFactory(identifier="section")

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
            # create the folio with factor_boy
            folio_obj = FolioFactory(identifier=folio_identifier, facsimile=facsimile,
                                     number=folio_count[folio_identifier])
            assert folio_obj.identifier == folio_identifier

            if folio_identifier in folio_count and folio_count[folio_identifier] > 1:
                # Set the previous_folio field to the previous Folio object
                folio_obj.previous_folio = previous_folio_obj
            previous_folio_obj = folio_obj  # Update the previous Folio object
            folio_obj.save()

            # Get or create a Line object with the specified line ID
            line_obj = SectionFactory(section_type=line_section_type, identifier=line_identifier, text=text)
            # Check if this is the first time the line has been encountered
            if line_identifier in line_count and line_count[line_identifier] > 1:
                # Set the previous_line field to the previous Line object
                line_obj.previous_line = previous_line_obj

            previous_line_obj = line_obj  # Update the previous Line object
            line_obj.save()

    print(f"Number of lines: {len(line_count)}")
    print(f"Number of folios: {len(folio_count)}")
    assert len(line_count) == 1
    assert len(folio_count) == 2

    return line_identifiers, folio_identifiers


fake = Faker()


@ pytest.fixture
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
