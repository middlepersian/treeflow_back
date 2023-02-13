import os
import json
import pytest
import pandas as pd
import numpy as np


from treeflow.corpus.models import Token, Section, SectionType, Section, Text, Corpus, Source, Dependency, Feature, Comment
from treeflow.dict.models import Lemma, Meaning
from treeflow.images.models import Image




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
        tokens, images, lines = parse_annotated(df)
        print()
        print("tokens {}".format(len(tokens)))
        print("images {}".format(len(images)))
        print("lines {}".format(len(lines)))

        #total number of sentences
        print("sentence objects {}".format(Section.objects.filter(section_type__identifier="sentence").count()))

        print("token objects {}".format(Token.objects.count()))
        print("lemma objects {}".format(Lemma.objects.count()))
        print("image objects {}".format(Image.objects.count()))
        print("line objects {}".format(Section.objects.filter(section_type__identifier="line").count()))
        #assert len(tokens) == 100

        for token_obj in Token.objects.all():
            print(token_obj.number, token_obj.number_in_sentence, token_obj.transliteration, token_obj.transcription)
            for deps in token_obj.dependencies.all():
                print('deps', deps.head, deps.head_number, deps.rel)

        print()
        '''
        for lemma_obj in Lemma.objects.filter().order_by('-created_at'):
            print('lemma', lemma_obj.word, lemma_obj.language, lemma_obj.multiword_expression, lemma_obj.related_meanings.all())
            for token in lemma_obj.token_lemmas.all():
                print('token', token.number, token.number_in_sentence, token.transliteration, token.transcription, token.upos)

            print()    
        '''    

@pytest.mark.django_db
def parse_annotated(df, text_object=None):
    # initialize variables
    current_newpart = None
    newparts = {}
    chapters = {}
    prev_chapter = None
    prev_section = None
    previous_folio_obj = None  # Initialize the previous_folio_obj variable
    previous_line_obj = None  # Initialize the previous_line_obj variable
    previous_token_obj = None  # Initialize the previous_token_obj variable
    previous_sentence_obj = None  # Initialize the previous_sentence_obj variable
    previous_image_obj = None
    sentence_obj = None


    corpus_object, corpus_created = Corpus.objects.get_or_create(slug="MPCD", name="Middle Persian Corpus and Dictionary")

    text_object, text_object_created = Text.objects.get_or_create(title="Greater Bundahišn or Iranian Bundahišn",  series="DMX", corpus=corpus_object, identifier="DMX-L19")
    assert text_object.title == "Greater Bundahišn or Iranian Bundahišn"
    assert text_object.series == "DMX"
    assert text_object.corpus.slug == "MPCD"

    #create source manuscript object
    manuscript_obj, manuscript_obj_created = Source.objects.get_or_create(type='manuscript', identifier='L19')

    # initialize sections
    # sentence section
    sentence_section_type, sentence_section_type_created = SectionType.objects.get_or_create(identifier="sentence")
    # line section
    line_section_type, line_section_type_created = SectionType.objects.get_or_create(identifier="line")
    # chapter section
    chapter_section_type, chapter_section_type_created = SectionType.objects.get_or_create(identifier="chapter")
    # section
    section_section_type, section_section_type_created = SectionType.objects.get_or_create(identifier="section")

    token_number = 1
    sentence_number = 1
    image_number = 1

    sentence_tokens = []
    tokens = []
    dependencies = []
    mwes = []
    lemmas = []
    images = []
    lines = set()
    parsed_sentences = []
 
    
    for i, row in df.iterrows():

        if i > 20:
            break
        token = None
        token_number_in_sentence = None
        transliteration = None
        transcription = None
        postag = None
        postfeatures = None
        newpart = None

        if sentence_obj:
            # check if at the end of the sentence
            if row.isna().all():
                print('### END_OF_SENTENCE', sentence_number)
            # process dependencies and their heads
                if dependencies:
                    print("### DEPS {}".format(len(dependencies)))
                    for dependency in dependencies:
                        # get head_number
                        head_number = float(dependency.head_number)
                        print("head_number {}".format(head_number))
                        assert head_number != None
                        #print('"head_number": {}'.format(head_number))
                        #check if token in list hast the same token_number_in_sentence as head
                        for token in sentence_tokens:
                            if token.number_in_sentence == head_number:
                                assert token.number_in_sentence != None
                                dependency.head = token
                                dependency.save()
                # process mwes
                if mwes:
                    print("mwes {}".format(mwes))
                    for mwe in mwes:
                        # split the mwe into its component lemmas
                        mwe_split = mwe.word.split()
                        for sub in mwe_split:
                                for lemma in lemmas:
                                    if sub in lemma.word:
                                        print("lemma {}".format(lemma.word))
                                        print("mwe {}".format(mwe))
                                        lemma.related_lemmas.add(mwe)
                                        lemma.save()                          
                # add tokens to sentence
                #check that tokens are not empty
                if tokens:
                    sentence_obj.tokens.add(*tokens)      
                    parsed_sentences.append(sentence_obj)   
                    sentence_obj.save()
                #clear up tokens list
                sentence_tokens = []    
                #clear up lemmas list
                lemmas = []
                #clear up dependencies list
                dependencies = []
                #clear up mwes list
                mwes = []
                sentence_number += 1
                previous_sentence_obj = sentence_obj    
                continue        

        if row["id"]:
            # new sentence
            if str(row["id"]).startswith("#SENTENCE"):
                #create sentence object
                sentence_obj, sentence_obj_created = Section.objects.get_or_create(section_type = sentence_section_type, number = str(sentence_number), identifier = text_object.identifier + "_sentence_" + str(sentence_number), text = text_object)
                print("#SENTENCE: {}".format(sentence_number))
                if previous_sentence_obj:
                    sentence_obj.previous = previous_sentence_obj
                    sentence_obj.save()
                else: 
                    sentence_obj.previous = None
                    sentence_obj.save()    
                continue         
                
            if str(row["id"]).startswith("#TRANSLATION"):
    
                #split the cell
                translation = str(row["id"]).split('=')
                if sentence_obj:
                    translation = translation[1]
                    if translation:
                        translation = normalize_nfc(input_string=translation)
                        meaning_obj, meaning_created = Meaning.objects.get_or_create(meaning=normalize_nfc(translation[1]), language="deu")
                        sentence_obj.meanings.add()
                        sentence_obj.save()
                        continue 
            if str(row["id"]).startswith("#COMMENT"):
    
                #split the cell
                comment = str(row["id"]).split('=')
                if sentence_obj:
                    comment = comment[1]
                    if comment:
                        comment = normalize_nfc(input_string=comment)
                        comment_obj = Comment.objects.create(comment=comment, section=sentence_obj)
                        continue                          

            #new token with number (word token)
            elif str(row["id"]) != "_":
                token_number_in_sentence = float(row["id"])
                print("token_number_in_sentence: {}".format(token_number_in_sentence))
            
        #check if transliteration value present
        if row["transliteration"] != "_" and pd.notna(row['transliteration']):
            transliteration = row["transliteration"]

        if row["transcription"] != "_" and pd.notna(row['transliteration']):
            transcription = row["transcription"]

        if row["postag"] != "_" and pd.notna(row['transliteration']) and row["postag"] != 'X':
            postag = row["postag"]

        # we do create a token if there is a transliteration or a token_number_in_sentence
        if transliteration or token_number_in_sentence:
            #create token object
            token, token_created = Token.objects.get_or_create(text = text_object, number = token_number)
            token.language = "pah"
            #increase token number
            if transliteration:
                token.transliteration = normalize_nfc(transliteration)
                assert token.transliteration == normalize_nfc(transliteration)
            assert token.number == token_number
            token_number += 1
    
            #add transcription
            if transcription:
                token.transcription = normalize_nfc(transcription)
                #print("token.transcription", token.transcription)
            #add postag
            if postag and postag != "X":
                token.upos = normalize_nfc(postag)
                assert token.upos == postag
            # if there is a number_in_sentence, then it is a word token    
            if token_number_in_sentence:
                #print(transcription, token_number_in_sentence)
                token.number_in_sentence = token_number_in_sentence
                token.word_token = True
            else: 
                token.word_token = False    

            #print("ix {} -  token {} - transliteration: {} - transcription: {} - postag: {}".format(i,token.number, token.transliteration, token.transcription, token.upos))    
            


        # process postfeatures
        if row["postfeatures"] != "_" and pd.notna(row['postfeatures']):    
            postfeatures = row["postfeatures"]
            #print("postfeatures {}".format( postfeatures))
            #print("postfeatures {}".format( postfeatures))
            #split postfeatures
            postfeatures = postfeatures.split("|")
            #create postfeatures
            postfeatures_to_add = []
            for postfeature in postfeatures:
                if postfeature and postfeature != "_":
                    if "=" in postfeature:
                        feature, value = postfeature.split("=")
                        # assert that the split existed and that the feature and value are not empty
                        assert feature and value
                        feature_obj, feature_obj_created = Feature.objects.get_or_create(feature=normalize_nfc(feature), feature_value=normalize_nfc(value))
                        postfeatures_to_add.append(feature_obj)
                    else: 
                        continue    
            else:
                postfeatures = None
            # add the to current token     
            if postfeatures_to_add:
                #assert token is not None
                token.features.add(*postfeatures_to_add)    


        # process dependencies
        if row["deprel"] != "_" :
            deprel = row["deprel"]
            #print("deprel {}".format( deprel))
            #get head
            if row["head"] and row["head"] != "_" and pd.notna(row['transliteration']):
                head = float(row["head"])
                #print("head {}".format( head))
                #create dependency
                dependency_obj, dependency_obj_created = Dependency.objects.get_or_create(head_number = head, rel = normalize_nfc(deprel))
                assert dependency_obj.head_number == head
                dependencies.append(dependency_obj)
                token.dependencies.add(dependency_obj)
        if row['deps'] != '_':
            deps = row['deps']
            # split on "|"
            deps = deps.split("|")
            for dep in deps:
                if dep and dep != "_":
                    head, rel = dep.split(":")
                    dependency_obj, dependency_obj_created = Dependency.objects.get_or_create(head_number = head, rel = normalize_nfc(deprel))
                    assert dependency_obj.head_number == head
                    dependencies.append(dependency_obj)


        # process lemmas
        # we need to be aware of MWEs. In the case of MWEs, only lemmas and meanings are present in the row
        if row['lemma'] != '_' and pd.notna(row['lemma']):
            lemma = row['lemma']
            lemma = normalize_nfc(input_string=lemma)
            if '$' != lemma and lemma != ',' and lemma != '$':
                print("### lemma: {}".format(lemma))
                # if token available, single lemma, if not, MWE
                if token:
                    # create lemma
                    lemma_obj, lemma_obj_created = Lemma.objects.get_or_create(word=normalize_nfc(lemma), multiword_expression=False, language="pah")
                    assert lemma_obj.multiword_expression == False
                    # add meaning
                    if row['meaning'] and row['meaning'] != '_' and pd.notna(row['meaning']):
                        meaning = row['meaning']
                        if ',' in meaning:
                            meaning = meaning.split(',')
                            for m in meaning:
                                m = m.strip()
                                m_obj, m_obj_created = Meaning.objects.get_or_create(meaning=normalize_nfc(m), language="eng")
                                lemma_obj.related_meanings.add(m_obj)        
                        else:
                            meaning_obj, meaning_obj_created = Meaning.objects.get_or_create(meaning=normalize_nfc(meaning), language="eng")
                            lemma_obj.related_meanings.add(meaning_obj)
                            token.meanings.add(meaning_obj)
                    lemmas.append(lemma)    
                    token.lemmas.add(lemma_obj)
                else:
                    #print("MWE: {}".format(lemma))
                    lemma_obj, lemma_obj_created = Lemma.objects.get_or_create(word=normalize_nfc(lemma), multiword_expression=True, language="pah")
                    assert lemma_obj.multiword_expression == True
                    # add meaning
                    if row['meaning'] != '_' and pd.notna(row['meaning']):
                        meaning = row['meaning']
                        if ',' in meaning:
                            meaning = meaning.split(',')
                            for m in meaning:
                                m = m.strip()
                                m_obj, m_obj_created = Meaning.objects.get_or_create(meaning=normalize_nfc(m), language="eng")
                                lemma.related_meanings.add(m_obj)
                        else:
                            m_obj, m_obj_created = Meaning.objects.get_or_create(meaning=normalize_nfc(meaning), language="eng")
                            lemma.related_meanings.add(m_obj)
                    mwes.append(lemma)    



        #process images
        if row['folionew'] != '_' and pd.notna(row['folionew']):
            img = row['folionew']
            #print("image {}".format(img))
            image_id = normalize_nfc(manuscript_obj.identifier + "_" + img)
            #print("image_id {}".format(image_id))
            image_obj, image_obj_created = Image.objects.get_or_create(identifier=image_id, source=manuscript_obj, number=image_number)
            #set source
            image_obj.source = manuscript_obj
            assert image_obj.identifier == image_id
            if previous_image_obj:
                image_obj.previous = previous_image_obj
                assert image_obj.previous == previous_image_obj
            #add to list
            images.append(image_obj)    
            previous_image_obj = image_obj
            image_number += 1


        # process lines
        if row['line'] != '_' and pd.notna(row['line']):

            # save line to image
            if previous_image_obj:
                line = row['line']
                img_name = previous_image_obj.identifier
                print("img_name {}".format(img_name))
                line_identifier = img_name + "_" + str(line)
                print("line_identifier {}".format(line_identifier))
                current_line_obj, current_line_obj_created = Section.objects.get_or_create(section_type=line_section_type, identifier = line_identifier)
                current_line_obj.number = float(line)
                assert current_line_obj.number == float(line)
                # add to list
                lines.add(current_line_obj)
                # save line to image
                previous_image_obj.sections.add(current_line_obj)
                previous_image_obj.save()    
                # update previous line
                previous_line_obj = current_line_obj 

        # process new_parts
        if row['newpart'] != '_' and not pd.isna(row['newpart']):
            # split the newpart string into chapter and section
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

            prev_chapter = chapter_obj


        if token:
            #add token to tokens list
            if previous_token_obj:
                token.previous = previous_token_obj
                assert token.previous == previous_token_obj
            token.save()
            previous_token_obj = token
            # for the record: it is actually previous_line_obj == current line obj
            if previous_line_obj:
                previous_line_obj.tokens.add(token)
                previous_line_obj.save()
            sentence_tokens.append(token)    
            tokens.append(token) 
            print('total deps: {}'.format(len(dependencies)))

    print("total tokens: {}".format(token_number)) 
    return tokens, images, lines



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

