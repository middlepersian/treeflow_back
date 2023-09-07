from asgiref.sync import sync_to_async
import strawberry
import strawberry_django
from strawberry import relay
from strawberry.tools import merge_types
from strawberry_django import mutations
from strawberry_django.mutations import resolvers
from strawberry_django.relay import ListConnectionWithTotalCount
from strawberry_django.permissions import IsAuthenticated, IsSuperuser
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry.django import auth
from typing import List, Optional, Dict, cast, Tuple
#corpus
from treeflow.corpus import models as corpus_models
from treeflow.corpus.types.bibliography import BibEntry, BibEntryInput, BibEntryPartial
from treeflow.corpus.models.bibliography import BibEntry as BibEntryModel
from treeflow.corpus.types.comment import Comment, CommentInput, CommentPartial
from treeflow.corpus.types.corpus import Corpus
from treeflow.corpus.enums.deprel import Deprel
from treeflow.corpus.types.dependency import Dependency, DependencyInput, DependencyPartial, DeprelList
from treeflow.corpus.types.feature import Feature, FeatureInput, FeaturePartial, PartOfSpeechFeatures, UPOSFeatures, UPOSList, get_features, upos_feature_feature_value
from treeflow.corpus.types.pos import POS, POSInput, POSPartial
from treeflow.corpus.enums.pos import UPOSValues
from treeflow.corpus.types.section import Section, SectionFilter, SectionInput, SectionPartial
from treeflow.corpus.models.section import Section as SectionModel
from treeflow.corpus.types.source import Source, SourceInput, SourcePartial
from treeflow.corpus.models.source import Source as SourceModel
#from treeflow.corpus.types.text_sigle import TextSigle
from treeflow.corpus.types.text import Text, TextFilter, TextInput, TextPartial
from treeflow.corpus.types.token import Token, TokenFilter, TokenInput, TokenPartial, TokenElastic, TokenSearchInput
from treeflow.corpus.documents.token import TokenDocument
from treeflow.corpus.types.user import User
#dict
from treeflow.dict import models as dict_models
from treeflow.dict.types.lemma import Lemma, LemmaInput, LemmaPartial, TermTechList, LanguageList
from treeflow.dict.types.meaning import Meaning, MeaningInput, MeaningPartial
from treeflow.dict.enums.term_tech import TermTech
from treeflow.dict.enums.language import Language
#image
from treeflow.images.types.image import Image, ImageInput, ImagePartial

#from treeflow.corpus.enums.comment_categories import CommentCategories
from elasticsearch_dsl import Search, Q, connections

###logging
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



@strawberry.type
class Query:

    ##corpus
    ### auth and users
    user: Optional[User] = strawberry_django.node(extensions=[IsSuperuser()])
    users:  relay.ListConnection[User] = strawberry_django.connection(extensions=[IsSuperuser()])
    me: User = auth.current_user()
    node: relay.Node = strawberry_django.node()
    # bibliography
    bib_entry: Optional[BibEntry] = strawberry_django.node()
    bib_entries:  ListConnectionWithTotalCount[BibEntry] = strawberry_django.connection()

    # comment
    comment: Optional[Comment] = strawberry_django.node()
    comments: ListConnectionWithTotalCount[Comment] = strawberry_django.connection()
    comments_list : List[Comment] = strawberry_django.field()

    # corpus
    corpus: Optional[Corpus] = strawberry_django.node()
    corpora: ListConnectionWithTotalCount[Corpus] = strawberry_django.connection()

    # dependency
    dependency: Optional[Dependency] = strawberry_django.node()
    dependencies: ListConnectionWithTotalCount[Dependency] = strawberry_django.connection()
    dependencies_list : List[Dependency] = strawberry_django.field()
    
    @strawberry.field
    def deprel_list(self, info) -> DeprelList:
        dep_list = [dep.value for dep in Deprel]
        return DeprelList(dep=dep_list)
    
    # feature
    feature: Optional[Feature] = strawberry_django.node()
    features: ListConnectionWithTotalCount[Feature] = strawberry_django.connection()
    features_list : List[Feature] = strawberry_django.field()

    @strawberry.field
    def get_features(self, pos: str) -> PartOfSpeechFeatures:
        feature_values = []
        for feature, values in get_features(pos).items():
            feature_values.append(UPOSFeatures(name=feature, values=values))
            
        return PartOfSpeechFeatures(pos=pos, features=list(get_features(pos).keys()), feature_values=feature_values)
    
    @strawberry.field
    def upos_list(self, info) -> UPOSList:
        pos_list = [pos.value for pos in UPOSValues]
        return UPOSList(pos=pos_list)


    # # pos
    pos: Optional[POS] = strawberry_django.node()
    pos_connection: ListConnectionWithTotalCount[POS] = strawberry_django.connection()
    pos_list : List[POS] = strawberry_django.field()

    # section
    section: Optional[Section] = strawberry_django.node()
    sections: ListConnectionWithTotalCount[Section] = strawberry_django.connection()
    sections_list : List[Section] = strawberry_django.field()

    @strawberry.field
    @sync_to_async
    def get_types(self) -> List[str]:
        section_types = SectionModel.objects.order_by('type').distinct('type').values_list('type', flat=True)
        return list(section_types)

    # source
    source: Optional[Source] = strawberry_django.node()
    sources: ListConnectionWithTotalCount[Source] = strawberry_django.connection()
    sources_list : List[Source] = strawberry_django.field()

    # text_sigle
    #text_sigle: Optional[TextSigle] = strawberry_django.node()
    #text_sigles:  relay.ListConnection[TextSigle] = strawberry_django.connection()

    # # text
    text: Optional[Text] = strawberry_django.node()
    texts: ListConnectionWithTotalCount[Text] = strawberry_django.connection()
    texts_list : List[Text] = strawberry_django.field()

    # # token
    token: Optional[Token] = strawberry_django.node()
    tokens: ListConnectionWithTotalCount[Token] = strawberry_django.connection()
    tokens_list : List[Token] = strawberry_django.field()

    @strawberry.field
    @sync_to_async
    def search_tokens(
        pattern: str,
        query_type: str,
        language: Optional[str] = None,
        pos: Optional[str] = None,
        size: int = 100
    ) -> List[TokenElastic]:

        q = Q(query_type, transcription=pattern)

        # Apply faceted search
        if language:
            q &= Q("term", language=language)
        if pos:
            q &= Q("nested", path="pos_token", query=Q("term", pos_token__pos=pos))

        response = TokenDocument.search().query(q).extra(size=size)

        logger.info(q.to_dict())
        logger.info(response.to_dict())

        tokens = []
        for hit in response:
            token = TokenElastic.from_hit(hit)
            tokens.append(token)

        return tokens

    @strawberry.field
    @sync_to_async
    def search_phrase_in_texts(
        self,
        tokens_to_search: List[TokenSearchInput],
        text_ids: List[str],
        size: int,
        ignore_stopwords: bool = False
    ) -> List[TokenElastic]:
        
        token_clauses = []
        span_near_clauses = []

        for token_input in tokens_to_search:
            query_field = token_input.field if token_input.field else "transcription"
            query_value = token_input.value if token_input.value else token_input.transcription
            if ignore_stopwords:
                query_field = f"{query_field}.no_stop"

            if token_input.query_type == "exact":
                token_q = Q("term", **{query_field: query_value})
                span_term_q = {"span_term": {query_field: query_value}}
                span_near_clauses.append(span_term_q)
            elif token_input.query_type == "wildcard":
                token_q = Q("wildcard", **{query_field: f"{query_value}*"})  
            elif token_input.query_type == "prefix":
                token_q = Q("prefix", **{query_field: query_value})
            elif token_input.query_type == "fuzzy":
                token_q = Q("fuzzy", **{query_field: query_value})
            elif token_input.query_type == "range":
                if token_input.start is None or token_input.end is None:
                    raise ValueError("Both start and end must be provided for range query")
                token_q = Q("range", **{query_field: {"gte": token_input.start, "lte": token_input.end}})
            elif token_input.query_type == "match":
                token_q = Q("match", **{query_field: query_value})
            else:
                raise ValueError(f"Unsupported query_type: {token_input.query_type}")

            if token_input.pos_token:
                pos_q = Q("term", pos=token_input.pos_token)
                token_clauses.append(Q('bool', must=[token_q, pos_q]))
            else:
                token_clauses.append(token_q)
        
        text_ids = [relay.from_base64(text_id)[1] for text_id in text_ids]
        text_q = Q("terms", **{"text.id": text_ids})
        
        if len(span_near_clauses) > 1:
            span_near_q = {
                "span_near": {
                    "clauses": span_near_clauses,
                    "slop": token_input.slop,
                    "in_order": True
                }
            }
            inner_bool_q = Q('bool', should=[Q(span_near_q)])
            final_q = Q('bool', must=[inner_bool_q, text_q])
        else:
            combined_token_q = Q('bool', should=token_clauses)
            final_q = Q('bool', must=[combined_token_q, text_q])

        logger.info(final_q.to_dict())
        response = TokenDocument.search().query(final_q).extra(size=size)
        logger.info(response.to_dict())
        tokens = [TokenElastic.from_hit(hit) for hit in response]

        return tokens


    @strawberry.field
    @sync_to_async
    def advanced_search_tokens(
        patterns: Optional[List[str]] = None,
        regex_patterns: Optional[List[str]] = None,
        lemma_ids: Optional[List[str]] = None,
        pos_tags: Optional[List[str]] = None,
        features: Optional[List[str]] = None,
        #metadata_conditions: Optional[Dict] = None,
        # ... other parameters
        #numerical_conditions: Optional[Dict] = None,
        scope: Optional[str] = None,
        range_within: Optional[int] = None,
        size: int = 100
    ) -> List[TokenElastic]:
        bool_query = Q("bool", should=[], minimum_should_match=1)
        
        # Handle exact match and wildcard patterns
        if patterns:
            for pattern in patterns:
                bool_query['bool']['should'].append(Q("wildcard", transcription=pattern))

        # Handle regex patterns
        if regex_patterns:
            for pattern in regex_patterns:
                bool_query['bool']['should'].append(Q("regexp", transcription=pattern))

        # Nested queries for lemmas, pos_tags, and features
        if lemma_ids:
            bool_query &= Q("nested", path="lemmas", query=Q("terms", lemmas__id=lemma_ids))
        if pos_tags:
            bool_query &= Q("nested", path="pos_token", query=Q("terms", pos_token__pos=pos_tags))
        if features:
            bool_query &= Q("nested", path="feature_token", query=Q("terms", feature_token__feature=features))

        # Metadata conditions (authors, annotators, etc.)
        if metadata_conditions:
            for field, value in metadata_conditions.items():
                bool_query &= Q("term", **{f"metadata.{field}": value})

        # Numerical conditions (greater than, less than etc.)
        if numerical_conditions:
            for field, (op, value) in numerical_conditions.items():
                if op == "gt":
                    bool_query &= Q("range", **{field: {"gt": value}})
                elif op == "lt":
                    bool_query &= Q("range", **{field: {"lt": value}})
                # ... other operators

        # Scope and Range conditions
        if scope == 'sentence':
            nested_query = Q("nested", 
                            path="tokens", 
                            query=Q("bool", 
                                    should=[Q(query_type, transcription=pattern) for pattern in patterns], 
                                    minimum_should_match=1
                                    )
                            )
            bool_query &= nested_query


        if range_within:
            pass
        # Execute the search query
        response = TokenDocument.search().query(bool_query).extra(size=size)
        tokens = [TokenElastic.from_hit(hit) for hit in response]
        return tokens

        

    # ### dict
    # # lemma
    lemma: Optional[Lemma] = strawberry_django.node()
    lemmas: ListConnectionWithTotalCount[Lemma] = strawberry_django.connection()
    lemmas_list : List[Lemma] = strawberry_django.field()

    @strawberry.field
    def term_tech_list(self, info) -> TermTechList:
        term_tech_list = [tt.value for tt in TermTech]
        return TermTechList(term_tech=term_tech_list)

    @strawberry.field
    def term_techs(self) -> List[str]:
        return [term_tech.value for term_tech in TermTech]    

    @strawberry.field
    def language_list(self, info) -> LanguageList:
        language_list = [l.value for l in Language]
        return LanguageList(language=language_list)    

    @strawberry.field
    def languages(self) -> List[str]:
        return [language.value for language in Language]

    # # meaning
    meaning: Optional[Meaning] = strawberry_django.node()
    meanings: ListConnectionWithTotalCount[Meaning] = strawberry_django.connection()
    meanings_list : List[Meaning] = strawberry_django.field()

    # ### image
    # # image
    image: Optional[Image] = strawberry_django.node()
    images: ListConnectionWithTotalCount[Image] = strawberry_django.connection()
    images_list : List[Image] = strawberry_django.field()



@strawberry.type
class Mutation:

    login: User = auth.login()
    logout = auth.logout()
    
    # bibliography
    create_bib_entry: BibEntry = mutations.create(BibEntryInput, extensions=[IsAuthenticated()])
    update_bib_entry: BibEntry = mutations.update(BibEntryPartial, extensions=[IsAuthenticated()])
    delete_bib_entry: BibEntry = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    # comment
    create_comment: Comment = mutations.create(CommentInput, extensions=[IsAuthenticated()])
    update_comment: Comment = mutations.update(CommentPartial, extensions=[IsAuthenticated()])
    delete_comment: Comment = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    # dependency
    create_dependency: Dependency = mutations.create(DependencyInput, extensions=[IsAuthenticated()])
    update_dependency: Dependency = mutations.update(DependencyPartial, extensions=[IsAuthenticated()])
    delete_dependency: Dependency = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    # feature
    create_feature: Feature = mutations.create(FeatureInput, extensions=[IsAuthenticated()])
    update_feature: Feature = mutations.update(FeaturePartial, extensions=[IsAuthenticated()])
    delete_feature: Feature = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    # pos
    create_pos: POS = mutations.create(POSInput, extensions=[IsAuthenticated()])
    update_pos: POS = mutations.update(POSPartial, extensions=[IsAuthenticated()])
    delete_pos: POS = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    # section
    create_section: Section = mutations.create(SectionInput, extensions=[IsAuthenticated()])
    update_section: Section = mutations.update(SectionPartial, extensions=[IsAuthenticated()])
    delete_section: Section = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    @strawberry_django.mutation(handle_django_errors=True)
    def set_previous_section(self, info, current_section: relay.GlobalID, previous_section: relay.GlobalID) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current = current_section.resolve_node_sync(info)
        previous = previous_section.resolve_node_sync(info)
        current.previous = previous
        current.save()
        return cast(Section, current)

    @strawberry_django.mutation(handle_django_errors=True)
    def create_section_between(self, info, previous_section: relay.GlobalID, new_section_data: SectionInput) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        data = vars(new_section_data)
        previous = previous_section.resolve_node_sync(info)
        new_section = resolvers.create(info, SectionModel, resolvers.parse_input(info, data))
        next_section = previous.next
        previous.next = new_section
        previous.save()
        if next_section:
            next_section.previous = new_section
            next_section.save()
        new_section.previous = previous
        new_section.next = next_section
        new_section.save()
        return cast(Section, new_section)

    @strawberry_django.mutation(handle_django_errors=True)
    def add_tokens_to_section(self, info, section: relay.GlobalID, tokens: List[relay.GlobalID]) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        section = section.resolve_node_sync(info)
        tokens = [token.resolve_node_sync(info) for token in tokens]
        section.tokens.set(tokens)
        section.save()
        return cast(Section, new_section)

    @strawberry_django.mutation(handle_django_errors=True)
    def create_section_between(self, info, previous_section: relay.GlobalID, new_section_data: SectionInput) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        data = vars(new_section_data)
        previous = previous_section.resolve_node_sync(info)
        new_section = resolvers.create(info, SectionModel, resolvers.parse_input(info, data))
        next_section = previous.next
        previous.next = new_section
        previous.save()
        if next_section:
            next_section.previous = new_section
            next_section.save()
        new_section.previous = previous
        new_section.next = next_section
        new_section.save()
        return cast(Section, new_section)

    @strawberry_django.mutation(handle_django_errors=True)
    def add_tokens_to_section(self, info, section: relay.GlobalID, tokens: List[relay.GlobalID]) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        section = section.resolve_node_sync(info)
        tokens = [token.resolve_node_sync(info) for token in tokens]
        section.tokens.set(tokens)
        section.save()
        return cast(Section, new_section)


    # source
    create_source: Source = mutations.create(SourceInput, extensions=[IsAuthenticated()])
    update_source: Source = mutations.update(SourcePartial, extensions=[IsAuthenticated()])
    delete_source: Source = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])


    @strawberry_django.mutation(handle_django_errors=True)
    def create_source_with_new_bibentry(self, info, source: SourceInput, bibentry: BibEntryInput) -> Source:
        if not info.context or not info.context.request.user.is_authenticated:
            raise Exception("Not authenticated")
        source =  vars(source)
        bibentry = vars(bibentry)
        #create bibentry
        new_bibentry = resolvers.create(info, BibEntryModel, resolvers.parse_input(info, bibentry))
        new_bibentry.save()
        #create source
        new_source = resolvers.create(info, SourceModel, resolvers.parse_input(info, source))
        # add bibentry to source
        new_source.references.add(new_bibentry)
        new_source.save()
        return cast(Source, new_source)   

    # text
    create_text: Text = mutations.create(TextInput, extensions=[IsAuthenticated()])
    update_text: Text = mutations.update(TextPartial, extensions=[IsAuthenticated()])
    delete_text: Text = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    # token
    create_token: Token = mutations.create(TokenInput, extensions=[IsAuthenticated()])
    update_token: Token = mutations.update(TokenPartial, extensions=[IsAuthenticated()])
    delete_token: Token = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])


    @strawberry_django.mutation(handle_django_errors=True)
    def create_token_between(self, info, previous_token: relay.GlobalID, new_token_data: TokenInput) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        data = vars(new_token_data)
        previous = previous_token.resolve_node_sync(info)
        new_token = resolvers.create(info, corpus_models.Token, resolvers.parse_input(info, data))
        next_token = previous.next
        previous.next = new_token
        previous.save()
        if next_token:
            next_token.previous = new_token
            next_token.save()
        new_token.previous = previous
        new_token.next = next_token
        new_token.save()
        return cast(Token, token)


    @strawberry_django.input_mutation(handle_django_errors=True)
    def join_tokens(self, info, current: relay.GlobalID, previous: relay.GlobalID,) -> Token:
        
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        
        current_token =  current.resolve_node_sync(info)
        previous_token =  previous.resolve_node_sync(info)
        current_token.previous = previous_token
        current_token.save()
        return cast(Token, token)


    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_lemmas_to_token(self, info,
                            token: relay.GlobalID,
                            lemmas: List[relay.GlobalID],
                            ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node_sync(info)
        lemmas = [lemma.resolve_node_sync(info) for lemma in lemmas]
        token.lemmas.add(*lemmas)
        token.save()
        return cast(Token, token)

    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_new_lemma_to_token(self, info,
                               token: relay.GlobalID,
                               lemma: LemmaInput,
                               ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node_sync(info)
        data = vars(lemma)
        lemma = resolvers.create(info, dict_models.Lemma, resolvers.parse_input(info, data))
        token.lemmas.add(lemma)
        token.save()
        return cast(Token, token)

    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_meanings_to_token(self, info,
                              token: relay.GlobalID,
                              meanings: List[relay.GlobalID],
                              ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node_sync(info)
        meanings = [meaning.resolve_node_sync(info) for meaning in meanings]
        token.meanings.add(*meanings)
        token.save()
        return cast(Token, token)

    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_new_meaning_to_token(self, info,
                                 token: relay.GlobalID,
                                 meaning: MeaningInput,
                                 ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node_sync(info)
        data = vars(meaning)
        meaning = resolvers.create(info, dict_models.Meaning, resolvers.parse_input(info, data))
        token.meanings.add(meaning)
        token.save()
        return cast(Token, token)


    @strawberry_django.input_mutation(handle_django_errors=True)
    def remove_lemmas_from_token(self,
                                 info,
                                 token: relay.GlobalID,
                                 lemmas: List[relay.GlobalID],
                                 ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node_sync(info)
        lemmas = [lemma.resolve_node_sync(info) for lemma in lemmas]
        token.lemmas.remove(*lemmas)
        token.save()
        return cast(Token, token)

    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_new_dependency_to_token(self, info,
                                    token: relay.GlobalID,
                                    dependency: DependencyInput,
                                    ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node_sync(info)
        data = vars(dependency)
        dependency = resolvers.create(info, corpus_models.Dependency, resolvers.parse_input(info, data))
        dependency.save()
        return cast(Token, token)

    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_new_pos_to_token(self, info,
                             token: relay.GlobalID,
                             pos: POSInput,
                             ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        data = vars(pos)
        token = token.resolve_node_sync(info)
        pos = resolvers.create(info, corpus_models.Pos, resolvers.parse_input(info, data))
        pos.save()
        return cast(Token, token)
        
    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_new_feature_to_token(self, info,
                                  token: relay.GlobalID,
                                  feature:FeatureInput,
                                  ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        data = vars(feature)
        token = token.resolve_node_sync(info)
        feature = resolvers.create(info, corpus_models.Feature, resolvers.parse_input(info, data))
        feature.save()
        return cast(Token, token)

    ## dict

    # lemma
    create_lemma: Lemma = mutations.create(LemmaInput, extensions=[IsAuthenticated()])
    update_lemma: Lemma = mutations.update(LemmaPartial, extensions=[IsAuthenticated()])
    delete_lemma: Lemma = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])

    @strawberry_django.mutation(handle_django_errors=True)
    def add_related_lemma_to_lemma(self, info, lemma: relay.GlobalID, related_lemma: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node_sync(info)
        related_lemma = related_lemma.resolve_node_sync(info)
        current_lemma.related_lemmas.add(related_lemma)
        current_lemma.save()
        return cast(Lemma, current_lemma)

    @strawberry_django.mutation(handle_django_errors=True)
    def add_new_related_lemma_to_lemma(self, info, lemma: relay.GlobalID, related_lemma: LemmaInput,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node_sync(info)
        #data = vars(related_lemma)
        related_lemma = resolvers.create(info, models.Lemma, resolvers.parse_input(info, data))
        current_lemma.related_lemmas.add(related_lemma)
        current_lemma.save()
        return cast(Lemma, current_lemma)

    @strawberry_django.mutation(handle_django_errors=True)
    def add_related_meaning_to_lemma(self, info, lemma: relay.GlobalID, related_meaning: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node_sync(info)
        related_meaning = related_meaning.resolve_node_sync(info)
        current_lemma.related_meanings.add(related_meaning)
        current_lemma.save()
        return cast(Lemma, current_lemma)

    @strawberry_django.mutation(handle_django_errors=True)
    def add_new_related_meaning_to_lemma(self, info, lemma: relay.GlobalID, related_meaning: MeaningInput,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node_sync(info)
        data = vars(related_meaning)
        related_meaning = resolvers.create(info, models.Meaning, resolvers.parse_input(info, data))
        current_lemma.related_meanings.add(related_meaning)
        current_lemma.save()
        return cast(Lemma, current_lemma)

    @strawberry_django.mutation(handle_django_errors=True)
    def remove_related_lemma_from_lemma(self, info, lemma: relay.GlobalID, related_lemma: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node_sync(info)
        related_lemma = related_lemma.resolve_node_sync(info)
        current_lemma.related_lemmas.remove(related_lemma)
        current_lemma.save()
        return cast(Lemma, current_lemma)

    @strawberry_django.mutation(handle_django_errors=True)
    def remove_related_meaning_from_lemma(self, info, lemma: relay.GlobalID, related_meaning: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node_sync(info)
        related_meaning = related_meaning.resolve_node_sync(info)
        current_lemma.related_meanings.remove(related_meaning)
        current_lemma.save()
        return cast(Lemma, current_lemma)


    # meaning
    create_meaning: Meaning = mutations.create(MeaningInput, extensions=[IsAuthenticated()])
    update_meaning: Meaning = mutations.update(MeaningPartial, extensions=[IsAuthenticated()])
    delete_meaning: Meaning = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])


    @strawberry_django.input_mutation(handle_django_errors=True)
    def add_related_meaning_to_meaning(self, info, meaning: relay.GlobalID, related: relay.GlobalID) -> Meaning:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        try:
            current_meaning = meaning.resolve_node_sync(info)
        except:
            raise Exception("Meaning not found.")
        try:
            related_meaning = related.resolve_node_sync(info)
        except:
            raise Exception("Related meaning not found.")
        current_meaning.related_meanings.add(related_meaning)
        current_meaning.save()
        return cast(Meaning, current_meaning)

    ## image
    create_image: Image = mutations.create(ImageInput, extensions=[IsAuthenticated()])
    update_image: Image = mutations.update(ImagePartial, extensions=[IsAuthenticated()])
    delete_image: Image = mutations.delete(strawberry_django.NodeInput, extensions=[IsAuthenticated()])




#MergedQuery = merge_types("MergedQuery", (Query, bibliography.Query, comment.Query, corpus.Query, dependency.Query, feature.Query, image.Query, lemma.Query, meaning.Query, pos.Query, section.Query, source.Query, text.Query, token.Query, user.Query))
#MergedMutation = merge_types("MergedMutation", (Mutation, bibliography.Mutation, comment.Mutation, dependency.Mutation, feature.Mutation, image.Mutation, lemma.Mutation, meaning.Mutation, pos.Mutation, section.Mutation, source.Mutation, text.Mutation, token.Mutation))
schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
