
import unicodedata
from treeflow.dict.models.lemma import Lemma

def normalize_nfc(input_string):
    input_string = input_string.strip()
    return unicodedata.normalize('NFC', input_string)

def get_lemma_by_id(lemma_id):
    return Lemma.objects.get(id=lemma_id)


def count_lemmas():
    return Lemma.objects.count()