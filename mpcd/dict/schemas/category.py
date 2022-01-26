from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Category


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {'category': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)

class CategoryInput(InputObjectType):
    category = String()

# Queries

class Query(ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

# Mutations

class CreateCategory(relay.ClientIDMutation):
    class Input:
        category = CategoryInput()

    category = Field(CategoryNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, category):
        # check that bybentry does not exist same title and year
        if Category.objects.filter(category=category).exists():
            return cls(success=False)

        else:
            category_instance = Category.objects.create(category=category)
            category_instance.save()
            return cls(category=category_instance, success=True)

class UpdateCategory(relay.ClientIDMutation):
    class Input:
        id = ID()
        category = CategoryInput()

    category = Field(CategoryNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, category):

        if Category.objects.filter(id=id).exists():

            category_instance = Category.objects.get(id=id)
            category_instance.category = category
            category_instance.save()

            return cls(category=category_instance, success=True)

        else:
            return cls(success=False)

class DeleteCategory(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):

        if Category.objects.filter(id=id).exists():
            Category.objects.get(id=id).delete()
            return cls(success=True)

        else:
            return cls(success=False)

class Mutation(ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()