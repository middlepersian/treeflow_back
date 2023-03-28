import pandas as pd
import string
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from treeflow.corpus.models import Token, Section, Section, Text, Corpus, Source, Dependency, Feature, Comment, POS
from treeflow.dict.models import Lemma, Meaning
from treeflow.images.models import Image
from django.conf import settings
from treeflow.utils.normalize import strip_and_normalize



def import_annotated_file(csv_file,manuscript_id, text_sigle, text_title ):


    # initialize variables
    prev_chapter = None
    prev_section = None
    previous_folio_obj = None  # Initialize the previous_folio_obj variable
    previous_line_obj = None  # Initialize the previous_line_obj variable
    previous_token_obj = None  # Initialize the previous_token_obj variable
    previous_sentence_obj = None  # Initialize the previous_sentence_obj variable
    previous_image_obj = None
    sentence_obj = None


    # normalize strings
    #manuscript_id = normalize_nfc(input_string=manuscript_id)
    #manuscript_id = manuscript_id.upper()
    #text_sigle = normalize_nfc(input_string=text_sigle)
    #text_sigle = text_sigle.upper()
    #text_title = normalize_nfc(input_string=text_title)
    text_title = text_title.title()

    #create source manuscript object
    #manuscript_id = "L19"
    manuscript_obj, manuscript_obj_created = Source.objects.get_or_create(type='manuscript', identifier=manuscript_id)

    #text_title = "Greater Bundahišn or Iranian Bundahišn"
    #text_sigle= "DMX"
    corpus_object, corpus_created = Corpus.objects.get_or_create(slug="MPCD", name="Middle Persian Corpus and Dictionary")
    text_identifier = text_sigle + "-" + manuscript_id

    text_object, text_object_created = Text.objects.get_or_create(title=text_title,  series=text_sigle, corpus=corpus_object, identifier=text_identifier)

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
    chapter_number = 1
    section_number = 1

    # read csv file
    df = pd.read_csv(csv_file, sep='\t', encoding='utf-8')
 
    
    for i, row in df.iterrows():

        token = None
        token_number_in_sentence = None
        transliteration = None
        transcription = None
        postag = None
        pos = None
        postfeatures = None
        newpart = None
    

        if sentence_obj:
            # check if at the end of the sentence
            if row.isna().all():
                print('### END_OF_SENTENCE', sentence_number)
                # process dependencies and their heads
                if dependencies:
                    #print("### DEPS {}".format(len(dependencies)))
                    for dependency in dependencies:
                        # get head_number
                        head_number = float(dependency.head_number)
                        #print("head_number {}".format(head_number))
                        assert head_number != None
                        #print('"head_number": {}'.format(head_number))
                        #check if token in list hast the same token_number_in_sentence as head
                        for stk in sentence_tokens:
                            if stk.number_in_sentence == head_number:
                                assert stk.number_in_sentence != None
                                dependency.producer = 1
                                dependency.head = stk
                                dependency.save()
                    #clear up dependencies list
                    dependencies.clear()            
                # process mwes
                if mwes:
                    #print("mwes {}".format(mwes))
                    for mwe in mwes:
                        # split the mwe into its component lemmas
                        mwe_split = mwe.word.split()
                        for sub in mwe_split:
                                for lemma in lemmas:
                                    if sub in lemma.word:
                                        #print("lemma {}".format(lemma.word))
                                        #print("mwe {}".format(mwe))
                                        lemma.related_lemmas.add(mwe)
                                        lemma.save()                          
                # add tokens to sentence
                #check that tokens are not empty
                if sentence_tokens:
                    sentence_obj.tokens.add(*sentence_tokens)      
                    parsed_sentences.append(sentence_obj)   
                    sentence_obj.save()
                #clear up tokens list
                sentence_tokens.clear()
                #clear up lemmas list
                lemmas.clear()
                #clear up mwes list
                mwes.clear()
                sentence_number += 1
                previous_sentence_obj = sentence_obj    
                continue        

        if row["id"]:
            # new sentence
            if str(row["id"]).startswith("#SENTENCE"):
                #create sentence object
                sentence_obj, sentence_obj_created = Section.objects.get_or_create(type = "sentence", number = str(sentence_number), identifier = text_object.identifier + "_sentence_" + str(sentence_number), text = text_object)
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
                        meaning_obj, meaning_created = Meaning.objects.get_or_create(meaning=strip_and_normalize('NFC', translation), language="deu", lemma_related=False)
                        sentence_obj.meanings.add(meaning_obj)
                        sentence_obj.save()
                        continue 
            if str(row["id"]).startswith("#COMMENT"):
    
                #split the cell
                comment = str(row["id"]).split('=')
                if sentence_obj:
                    if comment[1]:
                        Comment.objects.create(comment=comment[1], section=sentence_obj)
                        continue                          

            #new token with number (word token)
            elif str(row["id"]) != "_":
                token_number_in_sentence = float(row["id"])
                #print("token_number_in_sentence: {}".format(token_number_in_sentence))
            
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
            token = Token.objects.create(text = text_object, number = token_number)
            token.language = "pal"
            #increase token numbe
            if transliteration:
                token.transliteration = transliteration
                assert token.transliteration == transliteration
            assert token.number == token_number
            token_number += 1
            #add transcription
            if transcription:
                token.transcription = transcription
                #print("token.transcription", token.transcription)
            #add upos

            # if there is a number_in_sentence, then it is a word token    
            if token_number_in_sentence:
                print(transcription, token_number_in_sentence)
                token.number_in_sentence = token_number_in_sentence
                assert token.number_in_sentence == token_number_in_sentence
                token.word_token = True
            else: 
                token.word_token = False    

        # process pos

        if postag and postag != "X":
            upos = postag
            pos, pos_created = POS.objects.get_or_create(pos=upos, type="upos", token=token)        
        # process postfeatures
        if row["postfeatures"] != "_" and pd.notna(row['postfeatures']):    
            postfeatures = row["postfeatures"]
            #split postfeatures
            postfeatures = postfeatures.split("|")
            #create postfeatures

            for postfeature in postfeatures:
                if postfeature and postfeature != "_":
                    if "=" in postfeature:
                        feature, value = postfeature.split("=")
                        # assert that the split existed and that the feature and value are not empty
                        assert feature and value
                        feature_obj = Feature.objects.create(feature=feature, feature_value=value, token=token, pos=pos)
                    else: 
                        continue    
            else:
                postfeatures = None
            # add the to current token     

        # process dependencies
        if row["deprel"] != "_" :
            deprel = row["deprel"]
            #print("deprel {}".format( deprel))
            #get head
            if row["head"] and row["head"] != "_" and pd.notna(row['transliteration']):
                head = float(row["head"])
                #print("head {}".format( head))
                #create dependency
                dependency_obj = Dependency.objects.create(head_number = head, rel =deprel, token=token)
                assert dependency_obj.head_number == head
                dependencies.append(dependency_obj)
                #check if root
                if deprel == 'root'  and token:
                    print("ROOT: {}".format(token))
                    token.root = True
        if row['deps'] != '_':
            deps = row['deps']
            # split on "|"
            deps = deps.split("|")
            for dep in deps:
                try:
                    if dep and dep != "_" and ':' in dep:
                        head, rel = dep.split(":")
                        head = float(head)
                        dependency_obj = Dependency.objects.create(head_number = head, rel = rel, token=token)
                        assert dependency_obj.head_number == head
                        dependencies.append(dependency_obj)
                except ValueError:
                    print("ValueError: {}".format(dep))
                    continue      
        # process lemmas
        # we need to be aware of MWEs. In the case of MWEs, only lemmas and meanings are present in the row
        if row['lemma'] != '_' and pd.notna(row['lemma']):
            lemma = row['lemma']
            if '$' != lemma and lemma != ',' and lemma != '$':
                #print("### lemma: {}".format(lemma))
                # if token available, single lemma, if not, MWE
                if token:
                    # create lemma
                    lemma_obj, lemma_obj_created = Lemma.objects.get_or_create(word=lemma, multiword_expression=False, language="pal")
                    # check if term.tech exists
                    if row['term._tech._(cat.)'] and row['term._tech._(cat.)'] != '_' and pd.notna(row['term._tech._(cat.)']): 
                        term_tech = row['term._tech._(cat.)']
                        #print("term_tech: {}".format(term_tech))
                        #remove punctuation with translate
                        term_tech = term_tech.translate(str.maketrans('', '', string.punctuation))
                        lemma_obj.category = term_tech
                    # add meaning
                    if row['meaning'] and row['meaning'] != '_' and pd.notna(row['meaning']):
                        meaning = row['meaning']
                        if ',' in meaning:
                            meaning = meaning.split(',')
                            for m in meaning:
                                m = m.strip()
                                m_obj, m_obj_created = Meaning.objects.get_or_create(meaning=m, language="eng")
                                lemma_obj.related_meanings.add(m_obj)        
                        else:
                            meaning_obj, meaning_obj_created = Meaning.objects.get_or_create(meaning=meaning, language="eng")
                            lemma_obj.related_meanings.add(meaning_obj)
                            token.meanings.add(meaning_obj)
                    # save lemma
                    lemma_obj.save()        
                    lemmas.append(lemma_obj)    
                    token.lemmas.add(lemma_obj)
                else:
                    #print("MWE: {}".format(lemma))
                    lemma_obj, lemma_obj_created = Lemma.objects.get_or_create(word=lemma, multiword_expression=True, language="pal")
                    assert lemma_obj.multiword_expression == True
                    # add meaning
                    if row['meaning'] != '_' and pd.notna(row['meaning']):
                        meaning = row['meaning']
                        if ',' in meaning:
                            meaning = meaning.split(',')
                            for m in meaning:
                                m = m.strip()
                                m_obj, m_obj_created = Meaning.objects.get_or_create(meaning=m, language="eng")
                                lemma_obj.related_meanings.add(m_obj)
                        else:
                            m_obj, m_obj_created = Meaning.objects.get_or_create(meaning=meaning, language="eng")
                            lemma_obj.related_meanings.add(m_obj)
                    # save lemma
                    lemma_obj.save()        
                    mwes.append(lemma_obj)   
        #process images
        if pd.notna(row['folionew']):
            if row['folionew'] != '_':
                img = str(row['folionew'])
                #print("image {}".format(img))
                image_id = manuscript_obj.identifier + "_" + img
                #print("image_id {}".format(image_id))
                image_obj, image_obj_created = Image.objects.get_or_create(identifier=image_id, number=image_number)
                if image_obj_created:
                    image_obj.manuscript = manuscript_obj
                    image_obj.previous = previous_image_obj
                    try:
                            image_obj.save()
                    except IntegrityError as e:
                            image_obj.previous = None
                            image_obj.save()
                    #add to list
                    images.append(image_obj)    
                    previous_image_obj = image_obj
                    image_number += 1
            if previous_image_obj:
                # add token to image
                if token:
                    token.image = previous_image_obj
                
        # process lines
        if row['line'] != '_' and pd.notna(row['line']):
            # save line to image
            if previous_image_obj:
                line = row['line']
                img_name = previous_image_obj.identifier
                print("img_name {}".format(img_name))
                line_identifier = img_name + "_" + str(line)
                print("line_identifier {}".format(line_identifier))
                ## TODO Add text to line
                current_line_obj, current_line_obj_created = Section.objects.get_or_create(type="line",identifier = line_identifier, text=text_object)
                current_line_obj.number = float(line)
                assert current_line_obj.number == float(line)
                # set previous line
                if current_line_obj_created:
                    if previous_line_obj:
                        current_line_obj.previous = previous_line_obj
                        try:
                            current_line_obj.save()
                        except IntegrityError as e:
                                current_line_obj.previous = None
                                current_line_obj.save()
                    # add to list
                    lines.add(current_line_obj)
                    # update previous line
                    previous_line_obj = current_line_obj
                # save line to image
                previous_image_obj.sections.add(current_line_obj)
                previous_image_obj.save()    
                # update previous line
                previous_line_obj = current_line_obj 

        # process new_parts
        if not pd.isna(row['newpart']):
            #new part there
            if row['newpart'] != '_':
                # split the newpart string into chapter and section
                newpart = row['newpart']
                if not pd.isna(newpart) and newpart != '_':
                    # split the newpart string into chapter and section
                    newpart = str(newpart)
                    print('newpart', newpart)
                    source, chapter, section = newpart.split("_")
                    chapter = chapter.strip()
                    section = section.strip()
                    chapter_human = chapter.replace("ch", "chapter ")
                    section_human = section.replace("sec", "section ")
                        
                    # get or create the chapter object
                    chapter_identifier = source + '_' + chapter
                    assert chapter_identifier is not None
                    if token:
                        chapter_obj, chapter_obj_created = Section.objects.get_or_create(type="chapter", identifier=chapter_identifier, title = chapter_human, text=text_object)

                        if chapter_obj_created:
                            chapter_obj.number = chapter_number
                            chapter_number += 1
                            #chapter_obj.tokens.add(token)
                            # if the current chapter is not the same as the previous chapter
                            if prev_chapter:
                                if chapter_obj != prev_chapter:
                                    # set the current chapter as the previous chapter for the next iteration
                                    chapter_obj.previous = prev_chapter


                        # get or create the section object
                        section_identifier = source  + '_' +  chapter  + '_' +  section
                        assert section_identifier is not None
                        section_obj, section_obj_created = Section.objects.get_or_create(type="section", identifier=section_identifier, title = section_human, text=text_object)
                        if section_obj_created:
                            section_obj.number = section_number
                            section_number += 1
                            # if the current section is not the same as the previous section and belong to the same chapter
                            if prev_section:
                                if section_obj != prev_section and prev_section.container == chapter_obj:
                                    # set the current section as the previous section for the next iteration
                                    section_obj.previous = prev_section

                        
                        section_obj.container = chapter_obj
                        chapter_obj.tokens.add(token)
                        section_obj.tokens.add(token)
                        try:
                            section_obj.save()
                        except IntegrityError as e:
                            section_obj.previous = None
                            section_obj.save()
                        try:
                            chapter_obj.save()
                        except IntegrityError as e:
                            chapter_obj.previous = None
                            chapter_obj.save()
                        # update previous chapter and section
                        prev_chapter = chapter_obj
                        prev_section = section_obj
            else:
                # no new part
                # add token to previous section
                if token:
                    if prev_section:
                        prev_section.tokens.add(token)
                        prev_section.save()   
                    if prev_chapter:
                        prev_chapter.tokens.add(token)
                        prev_chapter.save()             

        #process comments
        if (row['comment'] != '_' and not pd.isna(row['comment'])) or (row['new_suggestion'] != '_' and not pd.isna(row['new_suggestion'])) or (row['uncertain'] != '_' and not pd.isna(row['uncertain'])) or (row['discussion'] != '_' and not pd.isna(row['discussion'])):  
            token_comment = row['comment']
            new_suggestion = row['new_suggestion']
            uncertain = row['uncertain']
            discussion = row['discussion']
            #print("comment: {}".format(comment))
            #print("new_suggestion: {}".format(new_suggestion))
            #print("uncertain: {}".format(uncertain))
            #print("discussion: {}".format(discussion))
            comment_obj = Comment()
            comment_obj.token = token
            if token_comment != '_' and not pd.isna(token_comment):
                comment_obj.comment = token_comment
            if new_suggestion != '_' and not pd.isna(new_suggestion):
                comment_obj.new_suggestion = [] 
                comment_obj.new_suggestion.append(new_suggestion)
            if uncertain != '_' and not pd.isna(uncertain):
                comment_obj.uncertain = [] 
                comment_obj.uncertain.append(uncertain)
            if discussion != '_' and not pd.isna(discussion):
                comment_obj.to_discuss = [] 
                comment_obj.to_discuss.append(discussion)
            comment_obj.save()    
        
        if token:
            #add token to tokens list
            if previous_token_obj:
                token.previous = previous_token_obj
                assert token.previous == previous_token_obj
                try:
                    token.save()
                except IntegrityError as e:
                    token.previous = None
                    token.save()
            else:         
                token.save()
            #set previous token
            previous_token_obj = token
            # for the record: it is actually previous_line_obj == current line obj
            if previous_line_obj:
                previous_line_obj.tokens.add(token)
                previous_line_obj.save()
            sentence_tokens.append(token)    
            tokens.append(token) 

    print("total tokens: {}".format(token_number)) 
    return tokens, images, lines


class Command(BaseCommand):
    help = 'Import file'

    def add_arguments(self, parser):
        #def parse_annotated(csv_file: str, manuscript_id:str, text_sigle:str, text_title:str ):

        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('manuscript_id', type=str, help='Manuscript ID e.g L19')
        parser.add_argument('text_sigle', type=str, help='Text sigle e.g. DMX')
        parser.add_argument('text_title', type=str, help='Text title e.g. Greater Bundahišn or Iranian Bundahišn')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        manuscript_id = kwargs['manuscript_id']
        text_sigle = kwargs['text_sigle']
        text_title = kwargs['text_title']

        settings.ELASTICSEARCH_DSL_AUTOSYNC = False
        settings.ELASTICSEARCH_DSL_AUTO_REFRESH = False
        
        tokens, images, lines= import_annotated_file(csv_file=csv_file, manuscript_id=manuscript_id, text_sigle=text_sigle, text_title=text_title)

        settings.ELASTICSEARCH_DSL_AUTOSYNC = True
        settings.ELASTICSEARCH_DSL_AUTO_REFRESH = True

        self.stdout.write(self.style.SUCCESS('Successfully imported {} tokens'.format(len(tokens))))
