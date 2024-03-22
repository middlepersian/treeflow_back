from django.core.management import BaseCommand
from django.core.cache import cache

from treeflow.corpus.models import Text, Token, Section
from treeflow.dict.models import Sense

from huey.contrib.djhuey import db_task

import logging
from uuid import UUID as uuid

logger = logging.getLogger(__name__)

COL_COUNT = 23

def token_to_conll(token:Token) -> str:
    sections = token.section_tokens.all()
    lemmas = token.lemmas.all()

    number_in_sentence = str(token.number_in_sentence) if token.number_in_sentence else "_"
    transcription = token.transcription if token.transcription else "_"
    head = "|".join([str(dep.head_number) if dep.head_number else "_" for dep in token.dependency_token.filter(enhanced=False)]) or "_"
    deprel = "|".join([str(dep.rel) if dep.rel else "_" for dep in token.dependency_token.filter(enhanced=False)]) or "_"
    deps = "|".join([f"{str(dep.head_number)}:{str(dep.rel)}" if dep.rel and dep.head_number else "_" for dep in token.dependency_token.filter(enhanced=True)]) or "_"
    transliteration = str(token.transliteration) if token.transliteration else "_"
    # folio
    folio = str(token.image.identifier) if token.image else "_"
    line = "|".join([str(line.number) if line.number else "_" for line in sections if line.type == "line"]) or "_"
    newParts = "|".join([str(section.identifier) for section in sections if section.type != "sentence" and section.type != "line"]) or "_"
    
    # Lemmas
    lemmaList =  [(str(lemma.word), str(lemma.language)) for lemma in lemmas] or "_"
    if lemmaList != "_":
        lemmas = "|".join([lemma[0] for lemma in lemmaList]) or "_"
        lemmaLangs = "|".join([lemma[1] for lemma in lemmaList]) or "_"
    else:
        lemmas = "_"
        lemmaLangs = "_"
    avestan = str(token.avestan) if token.avestan else "_"
    senses = "|".join([str(sense.sense) if sense.sense else "_" for sense in token.senses.all()]) or "_"
    pos = "|".join([str(pos.pos) if pos.pos else "_" for pos in token.pos_token.all()]) or "_"
    features = "|".join([f"{str(feature.feature)}={str(feature.feature_value)}" for feature in token.feature_token.all()]) or "_"
    
    comment, uncertrain, newSuggestions, discussion = comments_to_conll(token)
    # term_tech
    # TODO: term. tech. verknüpfen
    term_tech = "_"

    # literature
    literature = "_"

    # gloss
    gloss = token.gloss if token.gloss else "_"
    language = str(token.language) if token.language else "_"
    senses_lang = "|".join([str(sense.language) if sense.language else "_" for sense in token.senses.all()]) or "_"
    token_row = [
        number_in_sentence, transcription, head, deprel, deps, transliteration, folio ,line, newParts,
        lemmas, avestan, senses, pos, features, term_tech ,uncertrain, comment, 
        literature ,newSuggestions, discussion, gloss ,language, senses_lang, lemmaLangs
    ]

    return "\t".join(token_row)

def comments_to_conll(token:Token) -> list[str]:
    comments = token.comment_token.all()
    uncertrain = "|".join([str(comment.uncertain) for comment in comments]) or "_"
    comment = "|".join([str(comment.comment) for comment in comments]) or "_"
    newSuggestions = "|".join([str(comment.new_suggestion) for comment in comments]) or "_"
    discussion = "|".join([str(comment.to_discuss) for comment in comments]) or "_"
    return [comment, uncertrain, newSuggestions, discussion]

def sense_to_conll(sense:Sense) -> str:
    """ Returns a CoNLL line for a Sense object """
    return f"#TRANSLATION = {sense}"+"\t_"*(COL_COUNT-1)

def sentence_to_conll(section:Section) -> list[str]:
    """ Gets all tokens from a sentence and returns a list of CoNLL lines, one for each token, first items are the sentence metadata"""
    identifier = f"#SENTENCE ID = {section.identifier}"+"\t_"*(COL_COUNT-1) if section.identifier else "_\t_"*(COL_COUNT-1)
    translations = [sense_to_conll(sense) for sense in section.senses.all()]
    if not section.comment_section.all():
        comments = [f"#COMMENT ="+"\t_"*(COL_COUNT-1)]
    else:
        comments = [f"#COMMENT = {comment.comment}"+"\t_"*(COL_COUNT-1) for comment in section.comment_section.all()]
    tokens = [token_to_conll(token) for token in section.tokens.all()]
    return [identifier]+translations+comments+tokens+[' \t '*(COL_COUNT-1)]

@db_task()
def text_to_conll(text:Text, cache_key) -> list[str]:
    text_identifier = text.identifier
    logger.debug(f"Exporting Text {text_identifier} object with ID {text.id}")
    sentences = Section.objects.filter(text_id=text.id, type='sentence') \
            .order_by('number') \
            .prefetch_related("tokens", "senses", "comment_section" ,"tokens__lemmas", "tokens__pos_token", "tokens__image","tokens__feature_token", "tokens__comment_token")
    
    logger.debug(f"Found {len(sentences)} sentences")

    header = [
        "id", "transcription", "head", "deprel", "deps", "transliteration", "folionew", "line", "newpart",
        "lemma", "avestan", "meaning", "postag", "postfeatures", "term._tech._(cat.)", "uncertain", "comment",
        "literature", "new_suggestion", "discussion", "gloss", "token_lang", "meaning_lang", "lemma_langs"
    ]

    # header_row = "\t".join(header)
    conll = []
    if sentences:
        conll.append(header)
        for i,sentence in enumerate(sentences):
            sent = sentence_to_conll(sentence)
            for line in sent:
                conll.append(line.split("\t"))
            # log out 10% steps
            if i % (len(sentences)//10) == 0:
                logger.debug(f"Processed {i} sentences out of {len(sentences)} sentences. {i/len(sentences)*100:.2f}% done.")
            # log first sentence
            if i == 0:
                logger.debug(f"First sentence: {sent}")
    logger.debug("Done creating CoNLL file")

    cache.set(cache_key, {"status": "done", "data": conll})

    return conll



class Command(BaseCommand):
    """
    Exports a Text object to a CoNLL file
    Usage: python manage.py export_text <text_id> [--dry] [--verbosity <level>]
    """

    def add_arguments(self, parser):
        parser.add_argument('text_id', type=uuid, help='The ID of the Text object to export')

    def handle(self, *args, **options):
        text_id = options['text_id']
        text = Text.objects.get(id=text_id)
        

        logger.debug(f"Exporting Text object with ID {text_id}")
        sentences = Section.objects.filter(text_id=text_id, type='sentence') \
            .order_by('number') \
            .prefetch_related("tokens", "senses", "comment_section" ,"tokens__lemmas", "tokens__pos_token", "tokens__image","tokens__feature_token", "tokens__comment_token")
                       
        logger.debug(f"Found {len(sentences)} sentences")

        logger.debug("Dry run, not writing to file")

        header = [
            "id", "transcription", "head", "deprel", "deps", "transliteration", "folionew", "line", "newpart",
            "lemma", "avestan", "meaning", "postag", "postfeatures", "term._tech._(cat.)", "uncertain", "comment",
            "literature", "new_suggestion", "discussion", "gloss", "token_lang", "meaning_lang", "lemma_langs"
        ]

        header_row = "\t".join(header)


        if sentences:
            with open(f"{text.identifier}.conll.csv", 'w') as f:
                f.write(header_row + '\n')
                for i,sentence in enumerate(sentences):
                    sent = self.sentence_to_conll(sentence)
                    for line in sent:
                        f.write(line+'\n')
                    # log out 10% steps
                    if i % (len(sentences)//10) == 0:
                        logger.debug(f"Processed {i} sentences out of {len(sentences)} sentences. {i/len(sentences)*100:.2f}% done.")
                    # log first sentence
                    if i == 0:
                        logger.debug(f"First sentence: {sent}")
        logger.debug("Done creating CoNLL file")

    def token_to_conll(self,token:Token) -> str:
        sections = token.section_tokens.all()
        lemmas = token.lemmas.all()

        number_in_sentence = str(token.number_in_sentence) if token.number_in_sentence else "_"
        transcription = token.transcription if token.transcription else "_"
        head = "|".join([str(dep.head_number) if dep.head_number else "_" for dep in token.dependency_token.filter(enhanced=False)]) or "_"
        deprel = "|".join([str(dep.rel) if dep.rel else "_" for dep in token.dependency_token.filter(enhanced=False)]) or "_"
        deps = "|".join([f"{str(dep.head_number)}:{str(dep.rel)}" if dep.rel and dep.head_number else "_" for dep in token.dependency_token.filter(enhanced=True)]) or "_"
        transliteration = str(token.transliteration) if token.transliteration else "_"
        # folio
        folio = str(token.image.identifier) if token.image else "_"
        line = "|".join([str(line.number) if line.number else "_" for line in sections if line.type == "line"]) or "_"
        newParts = "|".join([str(section.identifier) for section in sections if section.type != "sentence" and section.type != "line"]) or "_"
        
        # Lemmas
        lemmaList =  [(str(lemma.word), str(lemma.language)) for lemma in lemmas] or "_"
        if lemmaList != "_":
            lemmas = "|".join([lemma[0] for lemma in lemmaList]) or "_"
            lemmaLangs = "|".join([lemma[1] for lemma in lemmaList]) or "_"
        else:
            lemmas = "_"
            lemmaLangs = "_"
        avestan = str(token.avestan) if token.avestan else "_"
        senses = "|".join([str(sense.sense) if sense.sense else "_" for sense in token.senses.all()]) or "_"
        pos = "|".join([str(pos.pos) if pos.pos else "_" for pos in token.pos_token.all()]) or "_"
        features = "|".join([f"{str(feature.feature)}={str(feature.feature_value)}" for feature in token.feature_token.all()]) or "_"
        
        comment, uncertrain, newSuggestions, discussion = self.comments_to_conll(token)
        # term_tech
        # TODO: term. tech. verknüpfen
        term_tech = "_"

        # literature
        literature = "_"

        # gloss
        gloss = token.gloss if token.gloss else "_"
        language = str(token.language) if token.language else "_"
        senses_lang = "|".join([str(sense.language) if sense.language else "_" for sense in token.senses.all()]) or "_"
        token_row = [
            number_in_sentence, transcription, head, deprel, deps, transliteration, folio ,line, newParts,
            lemmas, avestan, senses, pos, features, term_tech ,uncertrain, comment, 
            literature ,newSuggestions, discussion, gloss ,language, senses_lang, lemmaLangs
        ]

        return "\t".join(token_row)

    def comments_to_conll(self,token:Token) -> list[str]:
        comments = token.comment_token.all()
        uncertrain = "|".join([str(comment.uncertain) for comment in comments]) or "_"
        comment = "|".join([str(comment.comment) for comment in comments]) or "_"
        newSuggestions = "|".join([str(comment.new_suggestion) for comment in comments]) or "_"
        discussion = "|".join([str(comment.to_discuss) for comment in comments]) or "_"
        return [comment, uncertrain, newSuggestions, discussion]

    def sense_to_conll(self,sense:Sense) -> str:
        """ Returns a CoNLL line for a Sense object """
        return f"#TRANSLATION = {sense}"+"\t_"*(COL_COUNT-1)

    def sentence_to_conll(self,section:Section) -> list[str]:
        """ Gets all tokens from a sentence and returns a list of CoNLL lines, one for each token, first items are the sentence metadata"""
        identifier = f"#SENTENCE ID = {section.identifier}"+"\t_"*(COL_COUNT-1) if section.identifier else "_\t_"*(COL_COUNT-1)
        translations = [self.sense_to_conll(sense) for sense in section.senses.all()]
        if not section.comment_section.all():
            comments = [f"#COMMENT ="+"\t_"*(COL_COUNT-1)]
        else:
            comments = [f"#COMMENT = {comment.comment}"+"\t_"*(COL_COUNT-1) for comment in section.comment_section.all()]
        tokens = [self.token_to_conll(token) for token in section.tokens.all()]
        return [identifier]+translations+comments+tokens+[' \t '*(COL_COUNT-1)]

    