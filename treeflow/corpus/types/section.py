import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional, cast, Iterable
from strawberry.types.info import Info
from treeflow.corpus.types.token import Token, TokenElastic
# import value error
from django.core.exceptions import ValidationError
from builtins import ValueError


from treeflow.corpus import models

@strawberry_django.filters.filter(models.Section)
class SectionFilter:
    id: Optional[relay.GlobalID]
    type: strawberry.auto
    container: Optional['SectionFilter']
    tokens: Optional[strawberry.LazyType['TokenFilter', 'treeflow.corpus.types.token']]
    text:  Optional[strawberry.LazyType['TextFilter', 'treeflow.corpus.types.text']]
    image : Optional[strawberry.LazyType['ImageFilter', 'treeflow.images.types.image']]


@strawberry_django.type(models.Section, filters=Optional[SectionFilter])
class Section(relay.Node):
    comment_section: List[strawberry.LazyType['Comment', 'treeflow.corpus.types.comment']]
    
    id: relay.NodeID[str]
    number: strawberry.auto
    identifier: strawberry.auto
    title: strawberry.auto
    type: strawberry.auto
    text: Optional[strawberry.LazyType['Text', 'treeflow.corpus.types.text']]
    source:  Optional[strawberry.LazyType['Source', 'treeflow.corpus.types.source']]
    tokens: List[strawberry.LazyType['Token', 'treeflow.corpus.types.token']]
    meanings: List[strawberry.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    previous: Optional['Section']
    next: Optional['Section']
    container: Optional['Section']

    @strawberry_django.field(
        prefetch_related=["image_sections"])
    def resolve_image(self, info: Info) -> List[strawberry.LazyType['Image', 'treeflow.images.types.image']]:
        return [cast('Image', image) for image in self.image_sections.all().only("id", "identifier")]

    @strawberry_django.field(
        prefetch_related=[
            "section_container"
        ],
    )
    def contains_sections(self, info: Info) -> List[strawberry.LazyType['Section', 'treeflow.corpus.types.section']]:
        return [cast(Section, section) for section in self.section_container.all()]
    
    
    @strawberry_django.field(
        prefetch_related=[
            "tokens"
        ],
    )
    def resolve_tokens(self, info: Info) -> List[strawberry.LazyType['Token', 'treeflow.corpus.types.token']]:
        return [cast('Token', token) for token in self.tokens.all()]


    @strawberry_django.field(
        prefetch_related=[
            "meanings"
        ],
    )
    def resolve_meanings(self, info: Info) -> List[strawberry.LazyType['Meaning', 'treeflow.dict.types.meaning']]:
        return [cast('Meaning', meaning) for meaning in self.meanings.all()]     
    
@strawberry_django.input(models.Section)
class SectionInput:
    number: strawberry.auto
    identifier: strawberry.auto
    title: strawberry.auto
    text: strawberry.auto
    type: strawberry.auto
    source: strawberry.auto
    tokens: strawberry.auto
    meanings: strawberry.auto
    previous: strawberry.auto
    next: strawberry.auto
    container: strawberry.auto


@strawberry_django.partial(models.Section)
class SectionPartial:
    id: relay.GlobalID
    number: strawberry.auto
    title: strawberry.auto
    identifier: strawberry.auto
    text: strawberry.auto
    type: strawberry.auto
    source: strawberry.auto
    tokens: strawberry.auto
    previous: strawberry.auto
    meanings: strawberry.auto
    next: strawberry.auto
    container: strawberry.auto


class NotFoundError(Exception):
    """
    Custom exception to be raised when an item is not found.
    """
    def __init__(self, message="Item not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


@strawberry.type
class SectionElastic(relay.Node):
    id: relay.NodeID[str]  # Section ID
    text_id: str  # From the `text` object's `id`
    title: str  # From the `text` object's `title`
    type: str
    tokens: List[TokenElastic]
    
    @classmethod
    def from_hit(cls, hit):
        try:
            # Convert hit to dictionary if needed
            hit_dict = hit.to_dict() if hasattr(hit, 'to_dict') else hit
            
            # Validate and Extract fields
            text = hit_dict.get('text', {})
            if not text or 'id' not in text or 'title' not in text:
                raise ValueError("Invalid hit data. Missing 'text' details.")
            
            tokens_data = hit_dict.get('tokens', [])
            if not tokens_data:
                raise ValueError("Invalid hit data. Missing 'tokens'.")
            
            # Convert tokens
            tokens_elastic = [TokenElastic.from_hit(token_hit) for token_hit in tokens_data]
            
            return cls(
                id=hit_dict.get('id'),
                text_id=text.get('id'),
                title=text.get('title'),
                type=hit_dict.get('type'),
                tokens=tokens_elastic
            )
        except KeyError as e:
            raise ValueError(f"Missing key in hit data: {e}")

    @classmethod
    def resolve_id(cls, root: "SectionElastic", *, info: Info) -> str:
        return root.id
        

    @classmethod
    def resolve_node(cls, node_id: str, info: Optional[Info] = None, required: bool = False) -> Optional['SectionElastic']:
        try:
            node = get_section_by_id(id=relay.from_base64(node_id)[1])
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
            sections = get_sections_by_ids(ids=[relay.from_base64(gid)[1] for gid in node_ids])
            return [SectionElastic.from_hit(section) for section in sections]
        return []


def get_section_by_id(id: str) -> SectionElastic:
    s = Search(index='sections').query('ids', values=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise NotFoundError(f"No section by id {id}")

    return SectionElastic.from_hit(response.hits.hits[0]['_source'])


def get_sections_by_ids(ids: List[str]) -> List[SectionElastic]:
    s = Search(index='sections').query('ids', values=ids)
    response = s.execute()

    sections = []
    for hit in response.hits.hits:
        section = SectionElastic.from_hit(hit['_source'])
        sections.append(section)

    return sections


