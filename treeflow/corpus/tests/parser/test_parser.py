import os
import json
import pytest
import pandas as pd


##TODO normalize strings before saving to database

from treeflow.corpus.tests.factories.token import TokenFactory
from treeflow.corpus.tests.factories.section_type import SectionTypeFactory
from treeflow.corpus.tests.factories.section import SectionFactory
from treeflow.corpus.tests.factories.dependency import DependencyFactory


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
        if str(row["id"]).startswith("#SENTENCE_ID"):
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
        print(df.head())
        sentences = parse_sentences(df)
        parse_preannotated(sentences)


@pytest.mark.django_db
def test_parse_annotated():
    file = 'DMX-L19.csv'
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, file)
    with open(file_path, 'r') as f:
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        print(df.head())
        sentences = parse_sentences(df)
        parse_annotated(sentences)



@pytest.mark.django_db
def parse_preannotated(sentences, text_object=None):

    token_number = 1
    current_newpart = None
    newparts = {}
    newpart_number = 0
    sentence_id = ""
    for sentence in sentences:

        # initialize sections
        # sentence section
        sentence_section_type = SectionTypeFactory(identifier="sentence")
        # line section
        line_section_type = SectionTypeFactory(identifier="line")
        # chapter section
        chapter_section_type = SectionTypeFactory(identifier="chapter")
        # section
        section_section_type = SectionTypeFactory(identifier="section")

        for i, row in sentence.iterrows():
            token_id = row["id"]

            #check if token_id starts with #
            if str(token_id).strip().startswith("#"):
                if str(token_id).startswith("#SENTENCE_ID"):
                    sentence_id = str(token_id).split(" = ")[1]
                    assert sentence_id != ""
                elif str(token_id).startswith("#SENTENCE_TEXT"):
                    sentence_text = str(token_id).split(" = ")[1]
                    assert sentence_text != ""
                continue

            # assert token_id not empty
            assert token_id != ""
            # transcription
            transcription = row["transcription"]
            # assert transcription not empty
            assert transcription != ""
            # transliteration
            transliteration = row["transliteration"]
            # assert transliteration not empty
            assert transliteration != ""

            # create token

            token = TokenFactory(text=text_object, token_number=token_number)
            # create token transcription
            token.transcription = transcription
            token.transliteration = transliteration

            token_number += 1

            # postag
            postag = row["postag"]
            if postag != '_':
                postag = postag
            else:
                postag = None

            # postfeatures
            postfeatures = str(row["postfeatures"]).strip()
            postfeatures_to_add = []
            if postfeatures != '_':
                # create postfeatures (MorphologicalAnnotation)
                morpho_syntax = MorphologicalAnnotationFactory()
                if '|' in postfeatures:
                    # split postfeatures
                    postfeatures = postfeatures.split("|")
                    # sub split postfeatures
                    for postfeature in postfeatures:
                        postfeature = postfeature.split("=")
                        if len(postfeature) == 2:
                            feature = postfeature[0]
                            value = postfeature[1]
                            # create postfeature
                            postfeature = MorphologicalAnnotationFactory(
                                feature=feature, value=value)
                            postfeatures_to_add.append(postfeature)
                    else:
                        postfeatures = None

            # add postfeatures to token
            if postfeatures_to_add:
                token.morphological_annotation.add(*postfeatures_to_add)
            print("transcription {} - postfeatures: {}".format(transcription, postfeatures))

            # if there is a newpart, add it to the newparts dictionary
            if row["newpart"] == row["newpart"]:
                # check if newpart is not a digit or a _
                if str(row["newpart"]).strip():
                    # check if not _ or digit
                    if str(row["newpart"]).strip() != "_":
                        if not str(row["newpart"]).strip().replace('.', '').isdigit():
                            print("newpart: {} - sentence #{}".format(row["newpart"], sentence_id))

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
def parse_annotated(sentences, text_object=None):

    parsed_sentences = []

    current_newpart = None
    newparts = {}

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
    sentence_number = 1


    for sen_n, sentence in enumerate(sentences):

        # list of tokens in sentence
        tokens = []
        dependencies = []
        #create sentence
        print("SENTENCE #{}".format(sentence_number))
        sentence_obj = SectionFactory(section_type = sentence_section_type, number = sentence_number)
        assert sentence_obj.number == sentence_number

        sentence_number += 1

        for i, row in sentence.iterrows():
            token = None
            token_number_in_sentence = None
            transliteration = None
            transcription = None
            postag = None
            postfeatures = None
            newpart = None
            word_token = True

            try:                
                #check if id value present and is a digit
                if row["id"]:
                    # check if id value is a digit
                    if str(row["id"]).isdigit():
                        token_number_in_sentence = float(row["id"])
                        print("token_number_in_sentence: {}".format(token_number_in_sentence))


                #check if transliteration value present
                if row["transliteration"] and row["transliteration"] != "_" and pd.isna(row['transliteration']) == False:
                    transliteration = row["transliteration"]
                    print("transliteration:{}".format(transliteration))        

                if row["transcription"] and row["transcription"] != "_" and pd.isna(row['transliteration']) == False:
                    # assert row not nan
                    transcription = row["transcription"]
                    print("transcription:{}".format( transcription))

                if row["postag"] and row["postag"] != "_" and pd.isna(row['transliteration']) == False:
                    postag = row["postag"]
                    print("postag {}".format( postag))    

                if transliteration:
                    #create token
                    token = TokenFactory(text = text_object, token_number = token_number)
                    token.transliteration = transliteration
                    
                    #add token to tokens list
                    tokens.append(token)

                    #add transliteration
                    token.transliteration = transliteration
                    #add transcription
                    if transcription:
                        token.transcription = transcription
                    #add postag
                    if postag and postag != "X":
                        token.postag = postag
                    # if there is a number_in_sentence, then it is a word token    
                    if token_number_in_sentence:
                        token.token_number_in_sentence = token_number_in_sentence
                        token.word_token = True
                    else: 
                        token.word_token = False    

                    #increase token number
                    token_number += 1


                # process dependencies
                if row["deprel"] and row["deprel"] != "_" and pd.isna(row['transliteration']) == False:
                    deprel = row["deprel"]
                    print("deprel {}".format( deprel))
                    #get head
                    if row["head"] and row["head"] != "_" and pd.isna(row['transliteration']) == False:
                        head = row["head"]
                        print("head {}".format( head))
                        #create dependency
                        dependency = DependencyFactory(head_number = head, deprel = deprel)
                        dependencies.append(dependency)
                if row['deps'] and row['deps'] != '_' and pd.isna(row['transliteration']) == False:
                    deprel = row['deprel']
                    print("deprel {}".format(deprel))
                    # get head
                    if row['head'] and row['head'] != '_' and pd.isna(row['transliteration']) == False:
                        head = row['head']
                        print("head {}".format(head))
                        # create dependency
                        dependency = DependencyFactory(head_number=head, deprel=deprel)
                        dependencies.append(dependency)   
                
                if dependencies:
                    token.dependencies.add(*dependencies)     
                        
            except:
                pass    

        # process dependencies and their heads
        for dependency in dependencies:

            # get head_number
            head_number = dependency.head_number
            assert head_number != None
            #check if token in list hast the same token_number_in_sentence as head
            for token in tokens:
                if token.token_number_in_sentence == head_number:
                    assert token_number_in_sentence != None
                    assert token_number_in_sentence == head_number
                    dependency.head = token
                    dependency.save()

        # add tokens to sentence
        sentence_obj.tokens.add(*tokens)      
        parsed_sentences.append(sentence_obj)    

        
    return parsed_sentences

