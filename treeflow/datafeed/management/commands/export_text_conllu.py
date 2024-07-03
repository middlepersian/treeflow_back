from django.core.management import BaseCommand
from django.core.cache import cache

from treeflow.corpus.models import Text, Token, Section
from treeflow.dict.models import Sense

from huey.contrib.djhuey import db_task

import logging
from uuid import UUID as uuid

logger = logging.getLogger(__name__)


COL_COUNT = 10


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
        data = text_to_conllu(text,cache_key=text.identifier)
        


def token_to_conllu(token,number:int):
    token_row_list = []
    token_row_list.append(str(token.number_in_sentence) if token.number_in_sentence else "_")
    token_row_list.append(str(token.transcription or "_"))
    
    # get lemmas
    lemmas = token.lemmas.all()
    lemmaList =  [(str(lemma.word), str(lemma.language)) for lemma in lemmas] or "_"
    if lemmaList != "_":
        lemmas = "|".join([lemma[0] for lemma in lemmaList]) or "_"
    else:
        lemmas = "_"
    
    token_row_list.append(lemmas)

    pos = "|".join([str(pos.pos) if pos.pos else "_" for pos in token.pos_token.all()]) or "_"
    token_row_list.append(pos)
    token_row_list.append("_") # xpos

    features = "|".join([f"{str(feature.feature)}={str(feature.feature_value)}" for feature in token.feature_token.all()]) or "_"

    token_row_list.append(features)
    
    # faulty becaus reasignment of token number
    head = "|".join([str(dep.head_number) if dep.head_number else "_" for dep in token.dependency_token.filter(enhanced=False)]) or "_"
    
    token_row_list.append(head)

    deprel = "|".join([str(dep.rel) if dep.rel else "_" for dep in token.dependency_token.filter(enhanced=False)]) or "_"
    token_row_list.append(deprel)

    deps = "|".join([f"{str(dep.head_number)}:{str(dep.rel)}" if dep.rel and dep.head_number else "_" for dep in token.dependency_token.filter(enhanced=True)]) or "_"
    token_row_list.append(deps)

    senses = "|".join([str(sense.sense) for sense in token.senses.all()]) or "_"

    token_row_list.append(senses) # senses a misc

    token_row = "\t".join(token_row_list)

    return token_row

def sense_to_conllu(sense:Sense) -> str:
    """ Returns a CoNLL line for a Sense object """
    return f"#text_{sense.language} = {sense}"+"\t_"*(COL_COUNT-1)


def sentence_to_conllu(section:Section,p_text_identifier:str="") -> list[str]:
    """ Gets all tokens from a sentence and returns a list of CoNLL lines, one for each token, first items are the sentence metadata"""
    text_identifier = f"#text_id = {p_text_identifier}"+"\t_"*(COL_COUNT-1)
    identifier = f"#sent_id = {section.identifier}"+"\t_"*(COL_COUNT-1) if section.identifier else "_\t_"*(COL_COUNT-1)
    translations = [sense_to_conllu(sense) for sense in section.senses.all()]
    tokens = [token_to_conllu(token,j) for j,token in enumerate(section.tokens.all())]

    return [text_identifier]+[identifier]+translations+tokens+[' \t '*(COL_COUNT-1)]

@db_task()
def text_to_conllu(text:Text,cache_key) -> list[str]:
    text_identifier = text.identifier

    logger.debug("Creating CoNLL file")

    logger.debug(f"Exporting Text object with ID {text.id}")
    sentences = Section.objects.filter(text_id=text.id, type='sentence') \
        .prefetch_related("tokens", "senses","tokens__lemmas","tokens__senses","tokens__pos_token","tokens__feature_token","tokens__dependency_token") \
        .order_by('number')     
    logger.debug(f"Found {len(sentences)} sentences")
    if len(sentences) == 0:
        logger.debug("No sentences found")
        cache.set(cache_key, {"status": "error", "error": "No sentences found"})
        return []

    #           1     2      3      4      5       6      7       8        9     10
    header = ['id','form','lemma','upos','xpos','feats','head','deprel','deps','misc']

    conllu = []
    if sentences:
        conllu.append(header)

    for i,sentence in enumerate(sentences):
        text = sentence.identifier.split("_")[0].split("-")[:-1]
        text = "-".join(text)
        
        sent = sentence_to_conllu(sentence,text)
        for line in sent:
            conllu.append(line.split("\t"))
        
        if len(sentences)//10 > 0 and i % (len(sentences)//10) == 0:
            logger.debug(f"Processed {i} sentences out of {len(sentences)} sentences. {i/len(sentences)*100:.2f}% done.")
        
    logger.debug("Done creating CoNLL-U file")
    cache.set(cache_key, {"status": "done", "data": conllu})

    return conllu