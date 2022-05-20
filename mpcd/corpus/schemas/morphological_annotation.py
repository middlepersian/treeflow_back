from graphene import relay, InputObjectType, Field, ObjectType, ID, Boolean, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import MorphologicalAnnotation

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from .morphological_annotation_enums import ADJ, ADJNumType, ADJPoss, ADJNumber, ADJCase, ADJDegree, ADJVerbForm, ADJVoice, ADJPolarity


# TODO filter by feature in mutation

class MorphologicalAnnotationNode(DjangoObjectType):
    class Meta:
        model = MorphologicalAnnotation
        filter_fields = {'id': ['exact', 'icontains', 'istartswith'],
                         'feature': ['exact', 'icontains', 'istartswith'],
                         'feature_value': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class MorphologicalAnnotationInput(InputObjectType):
    feature = String()
    feature_value = String()

# Queries


class Query(ObjectType):
    morphological_annotation = relay.Node.Field(MorphologicalAnnotationNode)
    all_morphological_annotations = DjangoFilterConnectionField(MorphologicalAnnotationNode)

    adj_features = ADJ(required=True, adj_input=ADJ(required=True))
    adj_numtype = ADJNumType(required=True, adj_numtype_input=ADJNumType(required=True))
    adj_poss = ADJPoss(required=True, adj_poss_input=ADJPoss(required=True))
    adj_number = ADJNumber(required=True, adj_number_input=ADJNumber(required=True))
    adj_case = ADJCase(required=True, adj_case_input=ADJCase(required=True))
    adj_degree = ADJDegree(required=True, adj_degree_input=ADJDegree(required=True))
    adj_verbform = ADJVerbForm(required=True, adj_verbform_input=ADJVerbForm(required=True))
    adj_tense = ADJ(required=True, adj_tense_input=ADJ(required=True))
    adj_voice = ADJVoice(required=True, adj_voice_input=ADJVoice(required=True))
    adj_polarity = ADJPolarity(required=True, adj_polarity_input=ADJPolarity(required=True))

    def resolve_adj_features(root, info, adj_input):
        return adj_input

    def resolve_adj_numtype(root, info, adj_numtype):
        return adj_numtype

    @login_required
    def resolve_all_morphological_annotations(self, info, **kwargs):
        return gql_optimizer.query(MorphologicalAnnotation.objects.all(), info)

    def resolve_adj_poss(root, info, adj_poss):
        return adj_poss

    def resolve_adj_number(root, info, adj_number):
        return adj_number

    def resolve_adj_case(root, info, adj_case):
        return adj_case

    def resolve_adj_degree(root, info, adj_degree):
        return adj_degree

    def resolve_adj_verbform(root, info, adj_verbform):
        return adj_verbform

    def resolve_adj_tense(root, info, adj_tense):
        return adj_tense

    def resolve_adj_voice(root, info, adj_voice):
        return adj_voice

    def resolve_adj_polarity(root, info, adj_polarity):
        return adj_polarity

    def resolve_adj_features(root, info, adj_input):
        return adj_input

    def resolve_adj_numtype(root, info, adj_numtype):
        return adj_numtype

    @login_required
    def resolve_all_morphological_annotations(self, info, **kwargs):
        return gql_optimizer.query(MorphologicalAnnotation.objects.all(), info)


# Mutations

class CreateMorphologicalAnnotation(relay.ClientIDMutation):
    class Input:
        feature = String(required=True)
        feature_value = String(required=True)

    morphological_annotation = Field(MorphologicalAnnotationNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, feature, feature_value):

        morphological_annotation_instance = MorphologicalAnnotation.objects.get_or_create(
            feature=feature, feature_value=feature_value)
        morphological_annotation_instance.save()
        return cls(morphological_annotation=morphological_annotation_instance, success=True)


class UpdateMorphologicalAnnotation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        feature = String(required=True)
        feature_value = String(required=True)

    morphological_annotation = Field(MorphologicalAnnotationNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id, feature, feature_value):

        if MorphologicalAnnotation.objects.filter(pk=from_global_id(id)[1]).exists():
            morphological_annotation_instance = MorphologicalAnnotation.objects.get(pk=from_global_id(id)[1])
            morphological_annotation_instance.feature = feature
            morphological_annotation_instance.feature_value = feature_value
            morphological_annotation_instance.save()
            return cls(morphological_annotation=morphological_annotation_instance, success=True)

        else:
            return cls(success=False, morphological_annotation=None)


class DeleteMorphologicalAnnotation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        if MorphologicalAnnotation.objects.filter(id=id).exists():
            morphological_annotation_instance = MorphologicalAnnotation.objects.get(pk=from_global_id(id)[1])
            morphological_annotation_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_morphological_annotation = CreateMorphologicalAnnotation.Field()
    update_morphological_annotation = UpdateMorphologicalAnnotation.Field()
    delete_morphological_annotation = DeleteMorphologicalAnnotation.Field()
