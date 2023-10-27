import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional, cast, Iterable
from strawberry.types.info import Info
from treeflow.corpus.types.token import Token
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
    image: Optional[strawberry.LazyType['ImageFilter', 'treeflow.images.types.image']]


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


@strawberry.type
class HighlightedSection:
    section: Section
    highlighted_tokens: List[Token]

@strawberry.type
class HighlightedSectionConnection(relay.Connection[HighlightedSection]):
    DEFAULT_MAX_ITEMS_PER_PAGE = 10
    total_count: int = strawberry.field(default=0)

    @classmethod
    def resolve_connection(
        cls,
        nodes: Iterable[HighlightedSection],
        *,
        info: Optional[Info] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
    ):
        # Calculate total_count from the nodes
        total_count = len(nodes)
        # Use the section ID as the basis for pagination cursor
        edges_mapping = {
            relay.to_base64("section_id", str(section.section.id)): relay.Edge(
                node=section,
                cursor=relay.to_base64("section_id", str(section.section.id)),
            )
            for section in sorted(nodes, key=lambda s: s.section.id)
        }
        
        edges = list(edges_mapping.values())
        first_edge = edges[0] if edges else None
        last_edge = edges[-1] if edges else None

        if first is None and last is None:
            first = cls.DEFAULT_MAX_ITEMS_PER_PAGE

        if after is not None:
            after_edge_idx = edges.index(edges_mapping[after])
            edges = [e for e in edges if edges.index(e) > after_edge_idx]

        if before is not None:
            before_edge_idx = edges.index(edges_mapping[before])
            edges = [e for e in edges if edges.index(e) < before_edge_idx]

        if first is not None:
            edges = edges[:first]

        if last is not None:
            edges = edges[-last:]

    # Instead of calling super().resolve_connection, just return the connection
        return cls(
            edges=edges,
            total_count=total_count,
            page_info=strawberry.relay.PageInfo(
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None,
                has_previous_page=(
                    first_edge is not None and bool(edges) and edges[0] != first_edge
                ),
                has_next_page=(
                    last_edge is not None and bool(edges) and edges[-1] != last_edge
                ),
            ),
        )

