import os
import json
import pytest
import pandas as pd


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

from mpcd.dict.tests.factories.lemma import LemmaFactory
from mpcd.dict.tests.factories.meaning import MeaningFactory

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


@pytest.fixture
def sentences():
    file = 'sentences_10.json'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    with open(file_path, 'r') as f:
        sentences = json.load(f)
    return sentences


def parse_sentences(df):
    sentences = []
    sentence = pd.DataFrame(columns=df.columns)
    for i, row in df.iterrows():
        if str(row["id"]).startswith("#SENTENCE_ID"):
            sentences.append(sentence)
            sentence = pd.DataFrame(columns=df.columns)
        else:
            sentence = sentence.append(row)
    sentences.append(sentence)
    return sentences


@pytest.mark.django_db
def test_read_conll():
    file = 'Dk5_preannotated.csv'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    with open(file_path, 'r') as f:
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        print(df.head())
        sentences = parse_sentences(df)
        populate_db(sentences)


@pytest.mark.django_db
def test_read_file():
    file = 'GA_K20.xlsx'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)

    sentences = get_sentences(file_path)

    sentences = format_sentences(sentences)
    # serialize
    serialize_first_elements(sentences, 10)


@pytest.mark.django_db
def test_parse(sentences):
    # CREATE TEXT
    test_create_ga()

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

    assert len(line_identifiers) == 16
    assert len(folio_identifiers) == 2


@pytest.mark.django_db
def test_create_ga():
    codex_part = CodexPartFactory(codex__sigle="K20")
    facsimile = FacsimileFactory(bib_entry__key="zotero_k20", codex_part__codex__sigle="K20", codex_part__slug="k20new")
    text = TextFactory(title="Mādīgān ī Gizistag Abālīš", text_sigle__sigle="GA",
                       text_sigle__genre="andarz", corpus__slug="mpcd")
    assert text.title == "Mādīgān ī Gizistag Abālīš"
    assert text.text_sigle.sigle == "GA"
    assert text.corpus.slug == "mpcd"

    return text


@pytest.mark.django_db
def test_create_dmx():
    codex_part = CodexPartFactory(codex__sigle="K43a")
    facsimile = FacsimileFactory(bib_entry__key="zotero_K43a",
                                 codex_part__codex__sigle="K43a", codex_part__slug="K43anew")
    text = TextFactory(title="Dādestān ī mēnōy ī xrad", text_sigle__sigle="DMX",
                       text_sigle__genre="andarz",  corpus__slug="mpcd")
    assert text.title == "Dādestān ī mēnōy ī xrad"
    assert text.text_sigle.sigle == "DMX"
    assert text.corpus.slug == "mpcd"

    return text


@pytest.mark.django_db
def populate_db(sentences):

    token_number = 1
    current_newpart = None
    newparts = {}
    newpart_number = 0
    for sentence in sentences:
        for i, row in sentence.iterrows():
            token_id = row["id"]
            # assert token_id not empty
            assert token_id != ""
            token_number += 1
            # if there is a newpart, add it to the newparts dictionary
            if row["newpart"] == row["newpart"]:
                newpart = str(row["newpart"])
                if newpart.strip() not in ["_", ""]:
                    current_newpart = newpart
                    token_newpart = current_newpart
                    newpart_number += 1
                    newparts[newpart_number] = token_newpart
            assert current_newpart != ""
    print("Number of tokens: {}".format(token_number))
    print("Number of newparts: {}".format(newpart_number))


@pytest.mark.django_db
def parse_dict(sentences, facsimile,  line_identifiers, folio_identifiers, text):

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

    token_number = 1
    for sentence in sentences:
        for token_dict in sentence['tokens']:
            try:

                line_identifier = str(token_dict['folio']) + '_' + \
                    str(token_dict['line'])  # Initialize the line_id variable
                folio_identifier = facsimile.bib_entry.key + '_' + \
                    str(token_dict['folio'])  # Initialize the folio_id variable

                # Get or create a Token object with the specified token ID
                token_obj = TokenFactory(number=token_number, text=text,
                                         transcription=token_dict['transcription'], transliteration=token_dict['transliteration'])
                if token_dict.get('pos'):
                    token_obj.pos = token_dict['pos']
                lemma_obj = LemmaFactory(word=token_dict['lemma'], language='pah')
                token_obj.lemmas.add(lemma_obj)
                meaning_obj = MeaningFactory(meaning=token_dict['meaning'], language='eng')
                token_obj.meanings.add(meaning_obj)
                token_obj.save()

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

                # Get or create a Line object with the specified line ID
                line_obj = SectionFactory(section_type=line_section_type, identifier=line_identifier, text=text)
                # Check if this is the first time the line has been encountered
                if line_identifier in line_count and line_count[line_identifier] > 1:
                    # Set the previous_line field to the previous Line object
                    line_obj.previous = previous_line_obj

                previous_line_obj = line_obj  # Update the previous Line object
                # add token to line
                line_obj.tokens.add(token_obj)
                line_obj.save()

                # Get or create a Folio object with the specified folio ID
                # create the folio with factor_boy
                folio_obj = FolioFactory(identifier=folio_identifier, facsimile=facsimile,
                                         number=folio_count[folio_identifier])
                assert folio_obj.identifier == folio_identifier

                if folio_identifier in folio_count and folio_count[folio_identifier] > 1:
                    # Set the previous_folio field to the previous Folio object
                    folio_obj.previous = previous_folio_obj
                previous_folio_obj = folio_obj  # Update the previous Folio object
                folio_obj.sections.add(line_obj)
                folio_obj.save()

                # process sections
                # sentence section

                token_number += 1
            except Exception as e:
                print(e)
                print(token_dict)
                raise e

    print(f"Number of lines: {len(line_count)}, lines: {line_count}")
    print(f"Number of folios: {len(folio_count)}, folios: {folio_count}")
    print(f"Number of tokens: {token_number}")

    return line_identifiers, folio_identifiers
