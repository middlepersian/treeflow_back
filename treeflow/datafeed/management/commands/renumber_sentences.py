from treeflow.corpus.models import Text, Section, Token
from huey.contrib.djhuey import db_task

import logging
logger = logging.getLogger(__name__)

@db_task()
def renumber_sentences(text_id):
    """
    Renumber the sentences in a text
    """
    sections = Section.objects.filter(text_id=text_id, type="sentence").order_by('order')
    logger.debug("sections: %s" % sections)
    i = 1.0
    for section in sections:
        section.number = i
        section.save()
        i += 1.0