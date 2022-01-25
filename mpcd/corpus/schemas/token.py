from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models.dictionary import Entry
from mpcd.corpus.models import Token, Feature, FeatureValue, MorphologicalAnnotation, Pos, Dependency
from mpcd.corpus.schemas import MorphologicalAnnotationNode, MorphologicalAnnotationInput
from mpcd.corpus.schemas import PosNode, PosInput
from mpcd.corpus.schemas import DependencyNode, DependencyInput
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class TokenNode(DjangoObjectType):
    class Meta:
        model = Token
        filter_fields = {'transcription': ['exact', 'icontains', 'istartswith'],
                         'transliteration': ['exact', 'icontains', 'istartswith'],
                         'lemma': ['exact', 'icontains', 'istartswith'],
                         'pos': ['exact', 'icontains', 'istartswith'],
                         'morphological_annotation': ['exact', 'icontains', 'istartswith'],
                         'syntactic_annotation': ['exact', 'icontains', 'istartswith'],
                         'comment': ['exact', 'icontains', 'istartswith'],
                         'avestan': ['exact', 'icontains', 'istartswith'],
                         'previous': ['exact', 'icontains', 'istartswith'],
                         }
        interfaces = (relay.Node,)

class TokenInput(InputObjectType):
    transcription = String()
    transliteration = String()
    lemma = String()
    pos = String()
    morphological_annotation = String()
    syntactic_annotation = String()
    comment = String()
    avestan = String()
    previous = String()

