from ..models import Section

import logging

from django.shortcuts import render, get_object_or_404
import csv

from django.http import StreamingHttpResponse
# Set up logging
logger = logging.getLogger(__name__)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def resolve_sentence(reuquest, section_id=None):
    sentence = get_object_or_404(Section,id=section_id)
    meaning = sentence.senses.all()

    tokens = sentence.tokens.all()
    rows = []
    for token in tokens:
        row = tokenToConnl(token)
        rows.append(row)
        logger.debug(tokenToConnl(token))
    
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t')
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="sentence.csv"'}
    )

        


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

    logger.debug(f"""{number_in_sentence}\t{transcription}\t{head}\t{
            deprel}\t{
            deps}\t{
            transliteration}\t{
            line}\t{
            newParts}\t{
            lemmas}\t{
            lemmaLangs}\t{
            avestan}\t{
            senses}\t{
            pos}\t{
            features}\t{
            uncertrain}\t{
            comment}\t{
            newSuggestions}\t{
            discussion}\t{
            language}\t{
            senses_lang}"""
    )
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