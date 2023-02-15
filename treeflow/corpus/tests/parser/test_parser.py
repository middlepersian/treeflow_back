import os
import json
import pytest
import pandas as pd
import numpy as np
from django.db import IntegrityError


from treeflow.corpus.models import Token, Section, SectionType, Section, Text, Corpus, Source, Dependency, Feature, Comment
from treeflow.dict.models import Lemma, Meaning
from treeflow.images.models import Image


import logging

logger = logging.getLogger(__name__)

from treeflow.datafeed.utils import normalize_nfc
from treeflow.datafeed.management.commands.import_text import import_annotated_file

def serialize_first_elements(sentences, number_of_elements):
    file = 'sentences_{}.json'.format(number_of_elements)
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    jsonFile = open(file_path, "w")
    jsonFile.write(json.dumps(sentences[:number_of_elements], indent=4, ensure_ascii=False))


def parse_sentences(df):
    sentences = []
    sentence = pd.DataFrame(columns=df.columns)
    for i, row in df.iterrows():
        if str(row["id"]).startswith("#SENTENCE"):
            sentence = sentence.append(row)  # This line appends the current row to the sentence DataFrame
            sentences.append(sentence)
            sentence = pd.DataFrame(columns=df.columns)
        else:
            sentence = sentence.append(row)
    sentences.append(sentence)
    return sentences

@pytest.mark.django_db
def test_parse_preannotated():
    file = 'Dk5_preannotated.csv'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    with open(file_path, 'r') as f:
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        parse_preannotated(df)


@pytest.mark.django_db
def test_parse_annotated():
    file = 'DMX-L19.csv'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    manuscript_id = "L19"
    text_title = "Greater Bundahišn or Iranian Bundahišn"
    text_sigle= "DMX"
    tokens, images, lines = import_annotated_file(csv_file=file_path,text_sigle=text_sigle, text_title=text_title, manuscript_id=manuscript_id)
    print()
    '''
    print("tokens {}".format(len(tokens)))
    print("images {}".format(len(images)))
    print("lines {}".format(len(lines)))

    #total number of sentences
    print("sentence objects {}".format(Section.objects.filter(section_type__identifier="sentence").count()))

    print("token objects {}".format(Token.objects.count()))
    print("lemma objects {}".format(Lemma.objects.count()))
    # lemma as mwes
    print("lemma as mwe objects {}".format(Lemma.objects.filter(multiword_expression=True).count()))
    print("meaning objects {}".format(Meaning.objects.count()))
    # mwe objects
    print("image objects {}".format(Image.objects.count()))
    print("line objects {}".format(Section.objects.filter(section_type__identifier="line").count()))
    #assert len(tokens) == 100
    print("feature objects {}".format(Feature.objects.count()))
    '''

    for sentence in Section.objects.filter(section_type__identifier="sentence"):
        print('sentence', sentence.number)
        for meaning in sentence.meanings.all():
            print('meaning',meaning.meaning, meaning.language)
        for token in sentence.tokens.all():
            print('token', token.transcription, token.number_in_sentence)
            for dependency in token.dependencies.all():
                print('dependency',dependency.head, dependency.head_number, dependency.rel)
            print()
        print()




def test_escape_rows():
    allowed_values = [None, '', '_', np.nan]
    file = 'DMX-L19.csv'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    with open(file_path, 'r') as f:
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        for i, row in df.iterrows():
            is_row_valid = all(value in allowed_values for value in row.tolist())
            if is_row_valid:
                print(f"All values in row {i} are either None, NaN, '' or '_'", row)
            else:
                pass
                #print(f"Not all values in row {i} are either None, NaN, '' or '_'")

@pytest.mark.django_db
def test_read_newparts():
    file = 'DMX-L19.csv'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)

    corpus_object, corpus_created = Corpus.objects.get_or_create(slug="MPCD", name="Middle Persian Corpus and Dictionary")

    text_object, text_created = Text.objects.get_or_create(title="Greater Bundahišn or Iranian Bundahišn",  series="dmx", corpus=corpus_object)
    assert text_object.title == "Greater Bundahišn or Iranian Bundahišn"
    assert text_object.series == "dmx"
    assert text_object.corpus.slug == "MPCD"

    # chapter section
    chapter_section_type, chapter_section_type_created= SectionType.objects.get_or_create(identifier="chapter")
    # section
    section_section_type, section_section_type_created = SectionType.objects.get_or_create(identifier="section")

    # load the conll file into a pandas dataframe
    df = pd.read_csv(file_path, sep="\t")
    #print(df.head())
    chapters = {}
    prev_chapter = None
    prev_section = None

    for index, row in df.iterrows(): 
        newpart = row['newpart']
        if not pd.isna(newpart) and newpart != '_':
            # split the newpart string into chapter and section
            newpart = str(newpart)
            print('newpart', newpart)
            chapter, section = newpart.split(".")
            chapter = chapter.strip()
            section = section.strip()
            
            # get or create the chapter object
            chapter_identifier = 'dmx_' + chapter
            assert chapter_identifier is not None
            chapter_obj, chapter_obj_created = Section.objects.get_or_create(section_type=chapter_section_type, identifier=chapter_identifier, title = chapter, text=text_object)
            # if the current chapter is not the same as the previous chapter
            if prev_chapter:
                if chapter_obj != prev_chapter:
                    # create a new list for the current chapter in the chapters dictionary
                    chapters[chapter] = []
                    # set the current chapter as the previous chapter for the next iteration
                    chapter_obj.previous = prev_chapter
                    chapter_obj.save()
                    
            '''
            # section identifier
            section_identifier = 'dmx_' + chapter + '_' + section       
            assert section_identifier is not None

            section_obj, section_obj_created = Section.objects.get_or_create(section_type=section_section_type, identifier=section_identifier, title = chapter + '.' +section, text=text_object)     
            # check if object exists
            if section_obj_created:
                print("section_obj_created")
                # check that previous section is not the same as the current section
                if prev_section:
                    section_obj.previous = prev_section
                    print("section_obj", section_obj.identifier)
                    print("section_obj_previous", section_obj.previous.identifier)
                    section_obj.save()

            else:
                print("section_obj_exists")
            '''    
                      

            prev_chapter = chapter_obj
            #prev_section = section_obj


    for chap in Section.objects.filter(section_type=chapter_section_type).order_by('created_at'):
        print("chap_title", chap.title)
        if chap.previous:
            print("chap_previous",chap.previous.title)
    '''        
    print('####################')
    for sec in Section.objects.filter(section_type=section_section_type).order_by('created_at'):        

        if sec.previous:
            print("sec_chapter",sec.container.identifier)
            print("sec_title",sec.identifier)
            print("sec_previous",sec.previous.identifier)          

    print(chapters)
  '''

