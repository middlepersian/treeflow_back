import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional, Iterable, cast
from treeflow.corpus import models
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from asgiref.sync import sync_to_async


# create logger
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create console handler which logs messages with severity level INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)

@strawberry_django.filters.filter(models.Token, lookups=True)
class TokenFilter:

    id: Optional[relay.GlobalID]
    transcription: strawberry.auto
    transliteration: strawberry.auto
    language: strawberry.auto
    number: strawberry.auto
    text: Optional[strawberry.LazyType['TextFilter', 'treeflow.corpus.types.text']]
    image : Optional[strawberry.LazyType['ImageFilter', 'treeflow.images.types.image']]
    section_tokens: Optional[strawberry.LazyType['SectionFilter', 'treeflow.corpus.types.section']]


@strawberry_django.type(models.Token, filters=Optional[TokenFilter])
class Token(relay.Node):

    section_tokens: List[strawberry.LazyType['Section', 'treeflow.corpus.types.section']]
    comment_token: List[strawberry.LazyType['Comment', 'treeflow.corpus.types.comment']]
    feature_token : List[strawberry.LazyType['Feature', 'treeflow.corpus.types.feature']]
    pos_token : List[strawberry.LazyType['POS', 'treeflow.corpus.types.pos']]
    dependency_token : List[strawberry.LazyType['Dependency', 'treeflow.corpus.types.dependency']]

    id: relay.NodeID[str]
    number: strawberry.auto
    number_in_sentence: strawberry.auto
    root: strawberry.auto
    word_token: strawberry.auto
    visible: strawberry.auto
    text: Optional[strawberry.LazyType['Text', 'treeflow.corpus.types.text']]
    image:  Optional[strawberry.LazyType['Image', 'treeflow.images.types.image']] = None
    language: strawberry.auto
    transcription: strawberry.auto
    transliteration: strawberry.auto
    lemmas: List[strawberry.LazyType['Lemma', 'treeflow.dict.types.lemma']]
    meanings: List[strawberry.LazyType['Meaning', 'treeflow.dict.types.meaning']]

    avestan: strawberry.auto
    previous: Optional['Token']
    next: Optional['Token']

    gloss: strawberry.auto

    multiword_token: strawberry.auto
    related_tokens: List['Token']


@strawberry_django.input(models.Token)
class TokenInput:
    
    number: strawberry.auto
    number_in_sentence: strawberry.auto
    text: strawberry.auto
    image: strawberry.auto
    language: strawberry.auto
    transcription: strawberry.auto
    lemmas: strawberry.auto
    meanings: strawberry.auto
    avestan: strawberry.auto
    previous: strawberry.auto
    next: strawberry.auto
    gloss: strawberry.auto

    multiword_token: strawberry.auto
    related_tokens: strawberry.auto



@strawberry_django.partial(models.Token)
class TokenPartial:
    id: relay.GlobalID
    number: strawberry.auto
    number_in_sentence: strawberry.auto
    image: strawberry.auto
    text: strawberry.auto
    language: strawberry.auto
    transcription: strawberry.auto
    transliteration: strawberry.auto
    lemmas: strawberry.auto
    meanings: strawberry.auto

    avestan: strawberry.auto
    previous: strawberry.auto
    next: strawberry.auto
    gloss: strawberry.auto

    multiword_token: strawberry.auto
    related_tokens: strawberry.auto


# create input type for POS
@strawberry.input
class POSSelectionInput:
    pos: Optional[str]

# create input type for Feature
@strawberry.input
class FeatureSelectionInput:
    feature: Optional[str]
    feature_value: Optional[str]


@strawberry.input
class DistanceFromPreviousToken:
    distance: Optional[int] = None
    exact: Optional[bool] = False

@strawberry.input
class TokenSearchInput:
    query_type: Optional[str] = 'exact' # default to 'term'
    value: Optional[str] = None
    field: Optional[str] = 'transcription' # default to 'transcription'
    pos_token: Optional[List[POSSelectionInput]] = None
    feature_token: Optional[List[FeatureSelectionInput]] = None
    stopwords: Optional[bool] = False
    distance_from_previous: Optional[DistanceFromPreviousToken] = None
