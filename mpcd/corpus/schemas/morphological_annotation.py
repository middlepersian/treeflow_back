from graphene import relay, InputObjectType, Field, ObjectType, ID, Boolean, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import MorphologicalAnnotation

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


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
