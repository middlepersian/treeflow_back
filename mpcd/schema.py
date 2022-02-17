
import graphene
import mpcd.corpus.schemas
import mpcd.dict.schemas

## TODO check fields "!"

class Query(
        # Corpus Queries
        mpcd.corpus.schemas.author.Query,
        mpcd.corpus.schemas.bibliography.Query,
        mpcd.corpus.schemas.codex.Query,
        mpcd.corpus.schemas.codex_part.Query,
        mpcd.corpus.schemas.codex_token.Query,
        mpcd.corpus.schemas.corpus.Query,
        mpcd.corpus.schemas.dependency.Query,
        mpcd.corpus.schemas.facsimile.Query,
        mpcd.corpus.schemas.feature.Query,
        mpcd.corpus.schemas.feature_value.Query,
        mpcd.corpus.schemas.folio.Query,
        mpcd.corpus.schemas.line.Query,
        mpcd.corpus.schemas.morphological_annotation.Query,
        mpcd.corpus.schemas.pos.Query,
        mpcd.corpus.schemas.resource.Query,
        mpcd.corpus.schemas.section_type.Query,
        mpcd.corpus.schemas.text_sigle.Query,
        mpcd.corpus.schemas.text.Query,
        mpcd.corpus.schemas.token.Query,
        mpcd.corpus.schemas.section.Query,
        mpcd.corpus.schemas.sentence.Query,
        # Dict Queries
        mpcd.dict.schemas.category.Query,
        mpcd.dict.schemas.definition.Query,
        mpcd.dict.schemas.dictionary.Query,
        mpcd.dict.schemas.entry.Query,
        mpcd.dict.schemas.language.Query,
        mpcd.dict.schemas.lemma.Query,
        mpcd.dict.schemas.loanword.Query,
        mpcd.dict.schemas.reference.Query,
        mpcd.dict.schemas.translation.Query,
        graphene.ObjectType):
    pass


class Mutation(
        # Corpus Mutations
        mpcd.corpus.schemas.author.Mutation,
        mpcd.corpus.schemas.bibliography.Mutation,
        mpcd.corpus.schemas.codex.Mutation,
        mpcd.corpus.schemas.codex_part.Mutation,
        mpcd.corpus.schemas.codex_token.Mutation,
        mpcd.corpus.schemas.corpus.Mutation,
        mpcd.corpus.schemas.dependency.Mutation,
        mpcd.corpus.schemas.facsimile.Mutation,
        mpcd.corpus.schemas.feature.Mutation,
        mpcd.corpus.schemas.feature_value.Mutation,
        mpcd.corpus.schemas.folio.Mutation,
        mpcd.corpus.schemas.line.Mutation,
        mpcd.corpus.schemas.morphological_annotation.Mutation,
        mpcd.corpus.schemas.pos.Mutation,
        mpcd.corpus.schemas.resource.Mutation,
        mpcd.corpus.schemas.sentence.Mutation,
        mpcd.corpus.schemas.section.Mutation,
        mpcd.corpus.schemas.section_type.Mutation,
        mpcd.corpus.schemas.text_sigle.Mutation,
        mpcd.corpus.schemas.text.Mutation,
        mpcd.corpus.schemas.token.Mutation,
        # Dict Mutations
        mpcd.dict.schemas.category.Mutation,
        mpcd.dict.schemas.definition.Mutation,
        mpcd.dict.schemas.dictionary.Mutation,
        mpcd.dict.schemas.entry.Mutation,
        mpcd.dict.schemas.language.Mutation,
        mpcd.dict.schemas.lemma.Mutation,
        mpcd.dict.schemas.loanword.Mutation,
        mpcd.dict.schemas.reference.Mutation,
        mpcd.dict.schemas.translation.Mutation,
        graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
