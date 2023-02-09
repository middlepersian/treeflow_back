import os
import json
import pytest
import pandas as pd
import numpy as np


##TODO normalize strings before saving to database

from treeflow.corpus.tests.factories.token import TokenFactory
from treeflow.corpus.tests.factories.section_type import SectionTypeFactory
from treeflow.corpus.tests.factories.section import SectionFactory
from treeflow.corpus.tests.factories.dependency import DependencyFactory
from treeflow.corpus.tests.factories.postfeature import PostFeatureFactory
from treeflow.dict.tests.factories.lemma import LemmaFactory
from treeflow.dict.tests.factories.meaning import MeaningFactory
from treeflow.corpus.tests.factories.text import TextFactory


from treeflow.datafeed.utils import normalize_nfc


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
    with open(file_path, 'r') as f:
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        parse_annotated(df)



@pytest.mark.django_db
def parse_preannotated(sentences, text_object=None):

    set_of_values = [None, '', '_', np.nan]

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
                morpho_syntax = PostFeatureFactory()
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
                            postfeature = PostFeatureFactory(
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
def parse_annotated(df, text_object=None):

    parsed_sentences = []

    current_newpart = None
    newparts = {}

    line_count = {}
    folio_count = {}
    previous_folio_obj = None  # Initialize the previous_folio_obj variable
    previous_line_obj = None  # Initialize the previous_line_obj variable
    previous_token_obj = None  # Initialize the previous_token_obj variable
    previous_sentence_obj = None  # Initialize the previous_sentence_obj variable

    text_object = TextFactory(title="Test Text", corpus__slug = "MPCD", corpus__name = "Middle Persian Corpus and Dictionary")
    assert text_object.title == "Test Text"

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
    excluded_columns = ['lemma', 'meaning']

    # list of tokens in sentence
    tokens = []
    dependencies = []
    mwes = []
    lemmas = []
 
    sentence_obj = None
    
    for i, row in df.iterrows():
        token = None
        token_number_in_sentence = None
        transliteration = None
        transcription = None
        postag = None
        postfeatures = None
        newpart = None

        try:        
            #print("row: {}".format(row))        
            #check if id value present and is a digit
            if row["id"]:

                if str(row["id"]).startswith("#SENTENCE"):
                    #create sentence object
                    sentence_obj = SectionFactory(section_type = sentence_section_type, number = sentence_number, identifier = "sentence_{}".format(sentence_number), text = text_object)
                    print("#SENTENCE: {}".format(sentence_number))
                    if previous_sentence_obj:
                        sentence_obj.previous = previous_sentence_obj
                        sentence_obj.save()
                    else: 
                        sentence_obj.previous = None
                        sentence_obj.save()    
                    sentence_number += 1
                    previous_sentence_obj = sentence_obj
                    continue
                # check if id value is a digit
                elif pd.isna(row["id"]) or str(row["id"]) == '':
                    # new sentence, not a token
                    print("index", i)
                    continue
                elif str(row["id"]) != "_":
                    token_number_in_sentence = float(row["id"])
                    print("token_number_in_sentence: {} {}".format(token_number_in_sentence, token_number))
                
            #check if transliteration value present
            if row["transliteration"] != "_" and pd.notna(row['transliteration']):
                transliteration = row["transliteration"]
                print("transliteration:{}".format(transliteration), token_number_in_sentence)        

            if row["transcription"] != "_" and pd.notna(row['transliteration']):
                # assert row not nan
                transcription = row["transcription"]
                #print("transcription:{}".format( transcription))

            if row["postag"] != "_" and pd.notna(row['transliteration']) and row["postag"] != 'X':
                postag = row["postag"]
                #print("postag:{}".format(postag))

            if transliteration:
                print("transliteration: {}".format(transliteration))
                #create token
                token = TokenFactory(text = text_object, number = token_number)
                #increase token number
                token_number += 1
                assert token.text == text_object
                assert token.token_number == token_number
                #add transliteration
                token.transliteration = normalize_nfc(transliteration)
                #add transcription
                if transcription:
                    token.transcription = normalize_nfc(transcription)
                #add postag
                if postag and postag != "X":
                    token.postag = normalize_nfc(postag)
                # if there is a number_in_sentence, then it is a word token    
                if token_number_in_sentence != "_" and not np.isnan(token_number_in_sentence):
                    print(transcription, token_number_in_sentence)
                    token.token_number_in_sentence = token_number_in_sentence
                    token.word_token = True
                else: 
                    token.word_token = False    

                print("token #{} - transliteration: {} - transcription: {} - postag: {}".format(token_number, transliteration, transcription, postag))    

            

            # process postfeatures
            if row["postfeatures"] != "_" and pd.notna(row['postfeatures']):    
                postfeatures = row["postfeatures"]
                print("postfeatures {}".format( postfeatures))
                #print("postfeatures {}".format( postfeatures))
                # split postfeatures
                postfeatures = postfeatures.split("|")
                #create postfeatures
                postfeatures_to_add = []
                for postfeature in postfeatures:
                    if postfeature and postfeature != "_":
                        feature, value = postfeature.split("=")
                        # assert that the split existed and that the feature and value are not empty
                        assert feature and value
                        postfeature = PostFeatureFactory(feature=normalize_nfc(feature), value=normalize_nfc(value))
                        postfeatures_to_add.append(postfeature)
                else:
                    postfeatures = None
                # add the to current token     
                if postfeatures_to_add:
                    #assert token is not None
                    token.postfeatures.add(*postfeatures_to_add)    


            # process dependencies
            if row["deprel"] != "_" and pd.notna(row['transliteration']):
                deprel = row["deprel"]
                #print("deprel {}".format( deprel))
                #get head
                if row["head"] and row["head"] != "_" and pd.notna(row['transliteration']):
                    head = row["head"]
                    #print("head {}".format( head))
                    #create dependency
                    dependency = DependencyFactory(head_number = head, deprel = normalize_nfc(deprel))
                    assert dependency.head_number == head
                    dependencies.append(dependency)
            if row['deps'] != '_' and pd.notna(row['transliteration']):
                deprel = row['deprel']
                #print("deprel {}".format(deprel))
                # get head
                if row['head'] and row['head'] != '_' and pd.notna(row['transliteration']):
                    head = row['head']
                    #print("head {}".format(head))
                    # create dependency
                    dependency = DependencyFactory(head_number=head, deprel=normalize_nfc(deprel))
                    assert dependency.head_number == head
                    dependencies.append(dependency)   
            
            if dependencies:
                token.dependencies.add(*dependencies)     

            # process lemmas
            # we need to be aware of MWEs. In the case of MWEs, only lemmas and meanings are present in the row
            
            if row['lemma'] != '_' and pd.notna(row['lemma']):
                lemma = row['lemma']
                # check if lemma is a MWE
                to_check = row.drop(excluded_columns)
                # check if all the values are either NaN or '_'
                if (to_check.isna() | to_check.eq('_')).all():
                    # create MWE
                    print("MWE: {}".format(lemma))
                    assert lemma == 'passox kirdan' and row['meaning'] == 'answer'
                    lemma = LemmaFactory(lemma=normalize_nfc(lemma), multiword_expression=True)
                    assert lemma.multiword_expression == True
                    # add meaning
                    if row['meaning'] != '_' and pd.notna(row['meaning']):
                        meaning = row['meaning']
                        if ',' in meaning:
                            assert meaning == 'answer, reply'

                        #print("meaning {}".format(meaning))
                        meaning = MeaningFactory(meaning=normalize_nfc(meaning))
                        lemma.meanings.add(meaning)
                    mwes.append(lemma)    
                else:
                    # this is a single word lemma
                    if not lemma == '$':
                        print("lemma {}".format(lemma))

                        lemma = LemmaFactory(lemma=normalize_nfc(lemma), multiword_expression=False)
                        assert lemma.multiword_expression == False
                        # add meaning
                        if row['meaning'] and row['meaning'] != '_' and pd.notna(row['meaning']):
                            meaning = row['meaning']
                            #print("meaning {}".format(meaning))
                            meaning = MeaningFactory(meaning=normalize_nfc(meaning))
                            lemma.meanings.add(meaning)
                            token.meanings.add(meaning)
                        lemmas.append(lemma)    
                        token.lemmas = lemma

                        
            
                #add token to tokens list
            
            token.save()
            assert token.transliteration != None
            tokens.append(token)    

                    
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

    # process mwes
    if mwes:
        print("mwes {}".format(mwes))
        for mwe in mwes:
            # split the mwe into its component lemmas
            mwe_split = mwe.split()
            for sub in mwe_split:
                    # get the index of the mwe in the lemmas list
                    index = lemmas.index(sub)
                    # get the lemma object
                    lemma = lemmas[index]
                    # add the mwe to the lemma as related_lemma
                    lemma.related_lemma = mwe
                    assert lemma.related_lemma == mwe
                    lemma.save()

    # add tokens to sentence
    #check that tokens are not empty
    if tokens:

        sentence_obj.tokens.add(*tokens)      
        parsed_sentences.append(sentence_obj)   
    

    
    return parsed_sentences



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


