
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models


@gql.django.type(models.Text)
class Text:
    id: gql.auto
    corpus: 'Corpus'
    title: gql.auto
    text_sigle : 'TextSigle'
    editors: List['User']


