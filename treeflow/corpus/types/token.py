from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional

from treeflow.corpus import models



@gql.django.filters.filter(models.Text)
class TextFilter:
    id: relay.GlobalID
    title: gql.auto


@gql.django.filters.filter(models.Token, lookups=True)
class TokenFilter:
    id: relay.GlobalID
    transcription: gql.auto
    transliteration: gql.auto
    language: gql.auto
    number: gql.auto
    text: 'TextFilter'


@gql.django.type(models.Token, filters=TokenFilter)
class Token(relay.Node):

    section_tokens: List[gql.LazyType['Section', 'treeflow.corpus.types.section']]
    comment_token: List[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    number: gql.auto
    number_in_sentence: Optional[List[Optional[float]]]
    root: gql.auto
    word_token: gql.auto
    visible: gql.auto


    text: gql.LazyType['Text', 'treeflow.corpus.types.text']
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[gql.LazyType['Lemma', 'treeflow.dict.types.lemma']]
    meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    upos: gql.auto
    xpos: Optional[List[Optional[str]]]

    features: List[gql.LazyType['Feature', 'treeflow.corpus.types.feature']]
    dependencies: List[gql.LazyType['Dependency', 'treeflow.corpus.types.dependency']]
    avestan: gql.auto
    previous: Optional['Token']
    next: Optional['Token']

    gloss: gql.auto

    multiword_token: gql.auto
    related_tokens: List['Token']

    created_at: gql.auto
    updated_at: gql.auto


@gql.django.input(models.Token)
class TokenInput:
    number: gql.auto
    number_in_sentence: Optional[List[Optional[float]]]
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    upos: gql.auto
    xpos: Optional[List[Optional[str]]]
    features: gql.auto
    dependencies: gql.auto
    avestan: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto

    multiword_token: gql.auto
    related_tokens: gql.auto

    created_at: gql.auto
    updated_at: gql.auto


@gql.django.partial(models.Token)
class TokenPartial:
    id: relay.GlobalID
    number: gql.auto
    number_in_sentence: Optional[List[Optional[float]]]
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    upos: gql.auto
    xpos: Optional[List[Optional[str]]]
    features: gql.auto
    dependencies: gql.auto
    avestan: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto

    multiword_token: gql.auto
    related_tokens: gql.auto

    created_at: gql.auto
    updated_at: gql.auto
