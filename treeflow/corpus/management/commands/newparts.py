from django.core.management.base import BaseCommand
from treeflow.corpus.models import Section, Token, Text
from django.db.models import Q, QuerySet

import logging
logger = logging.getLogger(__name__)

def get_tokens_between_subsections(subsection_identifier:str) -> QuerySet:
    try:
        subsection_identifier = str(subsection_identifier)
    except ValueError:
        logger.info("Subsection identifier must be a string")
        return Token.objects.none()
    try:
        section = Section.objects.get(identifier=subsection_identifier)
    except Section.DoesNotExist:
        logger.info("Section with identifier {} does not exist".format(subsection_identifier))
        return Token.objects.none()
    text_id = section.text.id
    try:
        text = Text.objects.get(id=text_id)
    except Text.DoesNotExist:
        logger.info("Text with id {} does not exist".format(text_id))
        return Token.objects.none()
    
    # get next section of the same type
    try:
        next_section = Section.objects.filter(text__id=text.id).filter(type=section.type).filter(number__gt=section.number).order_by("number").prefetch_related("tokens").first()
    except Section.DoesNotExist:
        logger.info("No next section of type {} found".format(section.type))
        return Token.objects.none()

    if next_section:
        try:
            tokens = Token.objects.filter(Q(text__id=text.id)).filter(Q(number__range=[section.tokens.first().number, next_section.tokens.first().number-0.1]))
        except Token.DoesNotExist:
            logger.info("No tokens found")
            return Token.objects.none()
        return tokens
    return Token.objects.none()


class Command(BaseCommand):
    help = 'returns a list of all tokens in a chapter, between to subsubsections'

    def add_arguments(self, parser):
        parser.add_argument('subsection_identifier', type=str, help='subsections identifier')

    def handle(self, *args, **options):
        subsection_identifier = options['subsection_identifier']


        