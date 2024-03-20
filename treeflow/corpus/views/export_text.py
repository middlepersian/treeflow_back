from ..models import Section, Token, Text

import logging

from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from datetime import datetime

import csv

from django.http import StreamingHttpResponse
from treeflow.datafeed.management.commands.export_text import text_to_conll
# Set up logging
logger = logging.getLogger(__name__)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def resolve_text(request, text_id):
    # get Text 
    logger.debug(f"resolve_text: {text_id}")
    text = get_object_or_404(Text, id=text_id)
    # return text_to_conll(text=text)

    text_csv = text_to_conll(text=text)
    # check if text_csv is in cache
    # text_csv = cache.get(f"text_csv_{text_id}")
    # if not text_csv:
         
    #   text = Text.objects.prefetch_related(
    #     'section_text',
    #     'section_text__senses',
    #     'section_text__tokens',
    #     'section_text__tokens__lemmas',
    #     'section_text__tokens__dependency_token',
    #     'section_text__tokens__pos_token',
    #     'section_text__tokens__feature_token',
    #     'section_text__tokens__comment_token'
    #   ).get(id=text_id)
    #   # and prefetch all sections of type sentence
    #   logger.debug(f"prefetching done")
    #   sections = text.section_text.filter(type="sentence")
    #   rows = []
    #   for section in sections:
    #     rows += sentenceToConnl(section)

      
    #   text_csv = rows
    #   # cache text_csv
    #   cache.set(f"text_csv_{text_id}", text_csv, 60*60*24)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t')
    return StreamingHttpResponse(
        (writer.writerow(row) for row in text_csv),
        content_type="text/csv",
        headers={'Content-Disposition': f'attachment; filename="{text.identifier}.csv"'}
    )




def resolve_sentence(request, section_id=None):
    sentence = get_object_or_404(Section, id=section_id)
    rows = sentenceToConnl(sentence)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t')
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="sentence.csv"'}
    )

def sentenceToConnl(sentence):
    tokens = sentence.tokens.all()
    rows = []
    if tokens:
      rows = [tokenToConnl(token) for token in tokens]

    max_length = 20

    id_row = ['_']*max_length
    id_row[0] = f'#SENTENCE_ID = {sentence.identifier}'

    for translation in sentence.senses.all():
        translation_row = ['_']*max_length
        translation_row[0] = f'#TRANSLATION = {translation}'

        rows.insert(0, translation_row)
    rows.insert(0, id_row)
    rows.append(['']*max_length)

    return rows


def tokenToConnl(token):
    sections = token.section_tokens.all()
    lemmas = token.lemmas.all()

    number_in_sentence = str(token.number_in_sentence) if token.number_in_sentence else "_"
    transcription = token.transcription if token.transcription else "_"
    head = "|".join([str(dep.head_number) if dep.head_number else "_" for dep in token.dependency_token.all() if not dep.enhanced])
    deprel = "|".join([str(dep.rel) if dep.rel else "_" for dep in token.dependency_token.all() if not dep.enhanced])
    deps = "|".join([f"{str(dep.head_number)}:{str(dep.rel)}" if dep.rel and dep.head_number else "_" for dep in token.dependency_token.all() if dep.enhanced])
    transliteration = str(token.transliteration) if token.transliteration else "_"
    # folio
    line = "|".join([str(line.number) if line.number else "_" for line in sections if line.type == "line"])
    newParts = "|".join([str(section.identifier) for section in sections if section.type != "sentence" and section.type != "line"])
    
    # Lemmas
    lemmaList =  [(str(lemma.word), str(lemma.language)) for lemma in lemmas]

    lemmas = "|".join([lemma[0] for lemma in lemmaList])
    lemmaLangs = "|".join([lemma[1] for lemma in lemmaList])

    avestan = str(token.avestan) if token.avestan else "_"
    senses = "|".join([str(sense.sense) if sense.sense else "_" for sense in token.senses.all()])
    pos = "|".join([str(pos.pos) if pos.pos else "_" for pos in token.pos_token.all()])
    features = "|".join([f"{str(feature.feature)}={str(feature.feature_value)}" for feature in token.feature_token.all()])
    
    commentFields = packComments(token)
    # term_tech
    uncertrain = commentFields[1]
    comment = commentFields[0]
    # literature ?
    newSuggestions = commentFields[2]
    discussion = commentFields[3]
    # gloss
    language = str(token.language) if token.language else "_"
    senses_lang = "|".join([str(sense.language) if sense.language else "_" for sense in token.senses.all()])

    return [number_in_sentence,
                       transcription,
                         head,
                           deprel,
                             deps,
                               transliteration,
                                 line,
                                   newParts, 
                                   lemmas,
                                     lemmaLangs,
                                       avestan,
                                         senses,
                                           pos,
                                             features,
                                               uncertrain,
                                                 comment,
                                                   newSuggestions,
                                                     discussion,
                                                       language,
                                                         senses_lang]

def packComments(token):
    comments = token.comment_token.all()
    comment_col = "|".join([f"{str(comment.comment)}" if comment.comment else "_" for comment in comments])
    uncertain_col = "|".join([f"{str(comment.uncertain)}" if comment.uncertain else "_" for comment in comments])
    new_suggestion_col = "|".join([f"{str(comment.new_suggestion)}" if comment.new_suggestion else "_" for comment in comments])
    discussion_col = "|".join([f"{str(comment.to_discuss)}" if comment.to_discuss else "_" for comment in comments])

    return comment_col, uncertain_col, new_suggestion_col, discussion_col