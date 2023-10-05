import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional, Iterable, cast
from treeflow.dict.types.lemma import LemmaSelection, MeaningSelection
from treeflow.corpus import models
from elasticsearch_dsl import Search, connections, Q
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



@strawberry.type
class POSSelection:
    id: str
    pos: str

    @classmethod
    def from_hit(cls, hit):
        if 'pos_token' in hit:
            pos_tokens = hit['pos_token']
            return [cls(
                id=pos_token['id'],
                pos=pos_token['pos'],
            ) for pos_token in pos_tokens]
        return None

@strawberry.type
class FeatureSelection:
    id: str
    feature: str
    feature_value: str

    @classmethod
    def from_hit(cls, hit):
        if 'feature_token' in hit:
            feature_tokens = hit['feature_token']
            return[ cls(
                id=feature_token['id'],
                feature=feature_token['feature'],
                feature_value=feature_token['feature_value']
            ) for feature_token in feature_tokens]
        return None
        


@strawberry.type
class TokenSelection:
    id: Optional[str]
    number: Optional[float]
    number_in_sentence: Optional[float]
    transcription: Optional[str]
    transliteration: Optional[str]

    @classmethod
    def from_hit(cls, hit, field="next"):
        
        if field in hit and 'id' in hit[field]:
            return cls(
                id=hit[field].get('id'),
                number=hit[field].get('number'),
                number_in_sentence=hit[field].get('number_in_sentence'),
                transcription=hit[field].get('transcription'),
                transliteration=hit[field].get('transliteration')
            )
        return None


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
class TokenPositionInput:
    gap: Optional[int] = 0  # The gap of other tokens between them; default to 0



@strawberry.input
class TokenSearchInput:
    query_type: Optional[str]
    value: Optional[str]
    field: Optional[str] = 'transcription' # default to 'transcription'
    pos_token: Optional[List[POSSelectionInput]] = None
    feature_token: Optional[List[FeatureSelectionInput]] = None
    search_mode: Optional[str] = 'must' # default to 'must'#
    stopwords: Optional[bool] = False
    token_position: Optional[TokenPositionInput] = None


@strawberry.type
class TokenElastic(relay.Node):
    id: relay.NodeID[str]
    number: Optional[float] = None
    number_in_sentence: Optional[float] = None
    language: Optional[str] = None
    root: Optional[bool] = None
    word_token: Optional[bool] = None
    visible: Optional[bool] = None
    transcription: Optional[str] = None
    transliteration: Optional[str] = None
    avestan: Optional[str] = None
    gloss: Optional[str] = None
    next: Optional[TokenSelection] = None
    previous: Optional[TokenSelection] = None
    pos_token: Optional[List[POSSelection]] = None
    feature_token: Optional[List[FeatureSelection]] = None
    lemmas: Optional[List[LemmaSelection]] = None
    meanings: Optional[List[MeaningSelection]] = None
    highlight: Optional[bool] = False


    @classmethod
    def resolve_id(cls, root: "TokenElastic", *, info: Info) -> str:
        return root.id
    
    @classmethod
    def from_hit(cls, hit):
        # Convert the hit to a dictionary
        hit_dict = hit.to_dict() if hasattr(hit, 'to_dict') else hit        
        #logger.info(f"Processing hit: {hit_dict}")
        
        # Build and return a new instance of TokenElastic
        # TODO check fields like text and image thst are not necessary (siehe Token_object)
        return cls(
            id=relay.to_base64(TokenElastic, hit_dict.get('id', None)),
            number=hit_dict['number'] if 'number' in hit_dict else None,            
            language=hit_dict.get('language', None) if 'language' in hit_dict else None,
            root=hit_dict.get('root', None) if 'root' in hit_dict else None,
            word_token=hit_dict.get('word_token', None) if 'word_token' in hit_dict else None,
            visible=hit_dict.get('visible', None) if 'visible' in hit_dict else None,
            transcription=hit_dict.get('transcription', None) if 'transcription' in hit_dict else None,
            transliteration=hit_dict.get('transliteration', None) if 'transliteration' in hit_dict else None,
            avestan=hit_dict.get('avestan', None) if 'avestan' in hit_dict else None,
            gloss=hit_dict.get('gloss', None) if 'gloss' in hit_dict else None,
            pos_token=POSSelection.from_hit(hit_dict) if 'pos_token' in hit_dict else None,
            feature_token=FeatureSelection.from_hit(hit_dict) if 'feature_token' in hit_dict else None,
            next=TokenSelection.from_hit(hit_dict, field='next') if 'next' in hit_dict and hit_dict['next'] is not None else None,
            previous=TokenSelection.from_hit(hit_dict, field='previous') if 'previous' in hit_dict and hit_dict['previous'] is not None else None,
            lemmas=LemmaSelection.from_hit(hit_dict, field='lemmas') if 'lemmas' in hit_dict else None,
            meanings=MeaningSelection.from_hit(hit_dict, field='meanings') if 'meanings' in hit_dict else None,
            highlight=hit_dict.get('highlight', False)  # Set highlight based on hit data
        )



    @classmethod
    def resolve_node(cls, node_id: str, info: Optional[Info] = None, required: bool = False) -> Optional['TokenElastic']:
        try:
            node = get_token_by_id(id=relay.from_base64(node_id)[1])
            return node
        except (relay.GlobalIDValueError, NotFoundError):
            if required:
                raise ValueError(f"No node by id {node_id}")
            return None
        
    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: Optional[Info] = None,
        node_ids: Optional[Iterable[str]] = None
    ):
        if node_ids is not None:
            tokens = get_tokens_by_ids(ids=[relay.from_base64(gid)[1] for gid in node_ids])
            return [TokenElastic(id=relay.to_base64('TokenElastic', token['id']), **token) for token in tokens]

        return []



    @strawberry.field
    @sync_to_async
    def token_object(self, info: Optional[Info]) -> Optional[Token]:
        if self.id is not None:
            node_id = relay.from_base64(self.id)[1]
            token = models.Token.objects.get(id=node_id)
            return cast(Token,token)
        else:
            return None



def get_token_by_id(id: str) -> TokenElastic:
    s = Search(index='tokens').query('ids', values=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise NotFoundError(f"No token by id {id}")

    return TokenElastic.from_hit(response.hits.hits[0]['_source'])


def get_tokens_by_ids(ids: List[str]) -> List[TokenElastic]:
    s = Search(index='tokens').query('ids', values=ids)
    response = s.execute()

    tokens = []
    for hit in response.hits.hits:
        token = TokenElastic.from_hit(hit['_source'])
        tokens.append(token)

    return tokens
    
from elasticsearch_dsl.query import Q

def build_main_query(search_input: TokenSearchInput, stopwords: bool = False) -> Q:
    """Build and return the main query based on the given search input."""
    
    # Define a mapping from query_type to the corresponding Elasticsearch query function
    query_type_map = {
        'term': 'term',
        'range': 'range',
        'match': 'match',
        'match_phrase': 'match_phrase',
        'wildcard': 'wildcard',
        'fuzzy': 'fuzzy'
    }
    
    # Use the mapping to get the correct query type as a string
    query_type = query_type_map.get(search_input.query_type, 'term')
    
    # Modify the field if transcription and stopwords is True
    field_name = search_input.field
    if field_name == "transcription" and stopwords:
        field_name = "transcription.with_stops"
    
    # List of nested fields within 'tokens'
    nested_fields = ['lemmas', 'meanings', 'pos_token', 'feature_token', 'dependency_token', 'dependency_head']
    
    # Check for nested fields and handle them
    for nested_field in nested_fields:
        if nested_field in field_name:
            return Q('nested', 
                     path=f'tokens.{nested_field}', 
                     query=Q('bool', filter=[Q(query_type, **{f'tokens.{nested_field}.{field_name.split(".")[-1]}': search_input.value})])
                )
    
    # Build and return the query for other fields using filter context
    return Q('bool', filter=[Q(query_type, **{f'tokens.{field_name}': search_input.value})])


# Helper function to check if token matches criteria
def token_matches_criteria(token, criteria):
    return (
        (not criteria["transcription"] or token.get("transcription") == criteria["transcription"]) and
        (not criteria["transliteration"] or token.get("transliteration") == criteria["transliteration"]) and
        (not criteria["lemma"] or token.get("lemmas.word") == criteria["lemma"]) and
        (not criteria["pos"] or token.get("pos_token.pos") == criteria["pos"]) and
        (not criteria["feature"] or token.get("feature_token.feature") == criteria["feature"]) and
        (not criteria["feature_value"] or token.get("feature_token.feature_value") == criteria["feature_value"]) and
        (not criteria["dependency_rel"] or token.get("dependency_token.rel") == criteria["dependency_rel"]) and
        (not criteria["dependency_head_rel"] or token.get("dependency_head.rel") == criteria["dependency_head_rel"]) and
        (not criteria["meaning"] or token.get("meanings.meaning") == criteria["meaning"])
    )

def build_position_query(search_input: TokenSearchInput, position_input: TokenPositionInput) -> Q:
    """
    Build a position-based query based on the search and position inputs.

    :param search_input: The search input containing the field to search.
    :param position_input: The position input specifying the relative position.
    :return: A nested query targeting the specified position.
    """

    if not position_input or not hasattr(position_input, 'relative_to_token') or not hasattr(position_input, 'position'):
        raise ValueError("Invalid position_input provided!")

    # Begin by searching for the relative token
    relative_query = Q('term', **{f'tokens.{search_input.field}': position_input.relative_to_token})

    if position_input.position == "before":
        range_end = -1  # The token should be immediately before the relative token
        range_start = -(position_input.gap + 1)  # The token can be up to 'gap' tokens before the relative token
    elif position_input.position == "after":
        range_start = 1  # The token should be immediately after the relative token
        range_end = position_input.gap + 1  # The token can be up to 'gap' tokens after the relative token
    else:  # For "exact", we need the tokens to be adjacent
        range_start = 1
        range_end = 1


    # Construct the range query based on token's number
    range_query = Q('range', tokens__number={"gte": range_start, "lte": range_end})

    # Nest the queries to ensure they target the same section
    nested_query = Q(
        'nested',
        path='tokens',
        query=relative_query & range_query
    )

    return nested_query
