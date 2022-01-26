from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Entry, Lemma, Language, Translation
from mpcd.corpus.models import Token, Feature, FeatureValue, MorphologicalAnnotation, Pos, Dependency
from mpcd.corpus.schemas import MorphologicalAnnotationNode, MorphologicalAnnotationInput
from mpcd.corpus.schemas import PosNode, PosInput
from mpcd.corpus.schemas import DependencyNode, DependencyInput
from mpcd.dict.schemas import EntryNode, EntryInput
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TokenNode(DjangoObjectType):
    class Meta:
        model = Token
        filter_fields = {'transcription': ['exact', 'icontains', 'istartswith'],
                         'transliteration': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)


class TokenInput(InputObjectType):
    transcription = String()
    transliteration = String()
    lemma = EntryInput()
    pos = PosInput()
    morphological_annotation = List(MorphologicalAnnotationInput)
    syntactic_annotation = List(DependencyInput)
    comment = String()
    avestan = String()
    previous = TokenNode()

# Queries


class Query(ObjectType):
    token = relay.Node.Field(TokenNode)
    all_tokens = DjangoFilterConnectionField(TokenNode)

# Mutations


class CreateToken(relay.ClientIDMutation):
    class Input:
        transcription = String()
        transliteration = String()
        lemma = EntryInput()
        pos = PosInput()
        morphological_annotation = List(MorphologicalAnnotationInput)
        syntactic_annotation = List(DependencyInput)
        comment = String()
        avestan = String()
        previous = TokenNode()

    token = Field(TokenNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug("CreateToken.mutate_and_get_payload")
        if Token.objects.filter(id=input['id']).exists():
            return cls(errors=["Token with id {} already exists".format(input['id'])], success=False)
        else:
            token = Token.objects.create(transcription=input['transcription'], transliteration=input['transliteration'])
            if input['lemma']:
                if Entry.objects.filter(id=input['lemma']['id']).exists():
                    token.lemma = Entry.objects.get(id=input['lemma']['id'])
                # create the lemma
                else:
                    token_lemma = Lemma.objects.create(word=input['lemma']['word'])
                    token.lemma = token_lemma
                    # get lemma language
                    if Language.objects.filter(language=input['lemma']['language']).exists():
                        token_lemma.language = Language.objects.get(language=input['lemma']['language'])

                    # check for translations
                    if input['lemma']['translations']:
                        for translation in input['lemma']['translations']:
                            # if there is already a translation available
                            if Translation.objects.filter(meaning=translation.meaning).exists():
                                token_lemma.translations.add(Translation.objects.get(meaning=translation.meaning))
                            else:
                                local_translation = Translation.objects.create(meaning=translation.meaning)
                                if Language.objects.filter(language=translation.language).exists():
                                    local_translation.language = Language.objects.get(language=translation.language)
                                local_translation.save()
                                token_lemma.translations.add(local_translation)

                token_lemma.save()

            if input['pos']:
                if Pos.objects.filter(id=input['pos']['id']).exists():
                    token.pos = Pos.objects.get(id=input['pos']['id'])
                else:
                    token_pos = Pos.objects.create(pos=input['pos']['pos'])
                    token.pos = token_pos
                    token_pos.save()
            if input['morphological_annotation']:
                for annotation in input['morphological_annotation']:
                    if MorphologicalAnnotation.objects.filter(id=annotation['id']).exists():
                        token.morphological_annotations.add(MorphologicalAnnotation.objects.get(id=annotation['id']))
                    else:
                        if Feature.objects.filter(id=annotation['feature']['id']).exists():
                            token_feature = Feature.objects.get(id=annotation['feature']['id'])
                        else:
                            token_feature = Feature.objects.create(feature=annotation['feature']['identifier'])
                            token_feature.save()
                        if FeatureValue.objects.filter(id=annotation['feature_value']['id']).exists():
                            token_feature_value = FeatureValue.objects.get(id=annotation['feature_value']['id'])
                        else:
                            token_feature_value = FeatureValue.objects.create(
                                value=annotation['feature_value']['value'])
                            token_feature_value.save()
                        morphological_annotation = MorphologicalAnnotation.objects.create(
                            feature=token_feature, feature_value=token_feature_value)
                        token.morphological_annotations.add(morphological_annotation)
            if input['syntactic_annotation']:
                for annotation in input['syntactic_annotation']:
                    if Dependency.objects.filter(id=annotation['id']).exists():
                        token.syntactic_annotation.add(Dependency.objects.get(id=annotation['id']))
                    else:
                        token_dependency = Dependency.objects.create(head=annotation['head'], rel=annotation['rel'])
                        token.syntactic_annotation.add(token_dependency)

            if input['comment']:
                token.comment = input['comment']

            if input['avestan']:
                token.avestan = input['avestan']

            if input['previous']:
                if Token.objects.filter(id=input['previous']['id']).exists():
                    token.previous = Token.objects.get(id=input['previous']['id'])
                else:
                    return cls(errors=["Token with id {} does not exist".format(input['previous']['id'])],
                               success=False)
            token.save()

            return cls(token=token, success=True)
