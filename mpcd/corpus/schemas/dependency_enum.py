from graphene import Enum, ObjectType, Field


class DependencyEnum(Enum):
    adnominal_clause = 'acl'
    adverbial_clause_modifier = 'advcl'
    adverbial_modifier = 'advmod'
    adjectival_modifier = 'amod'
    appositional_modifier = 'appos'
    auxiliary = 'aux'
    case_marking = 'case'
    coordinating_conjunction = 'cc'
    clausal_complement = 'ccomp'
    compound = 'compound'
    conjunct = 'conj'
    copula = 'cop'
    determiner = 'det'
    discourse_element = 'discourse'
    fixed_multiword_expression = 'fixed'
    indirect_object = 'iobj'
    marker = 'mark'
    nominal_modifier = 'nmod'
    nominal_subject = 'nsubj'
    numeric_modifier = 'nummod'
    object = 'obj'
    oblique_nominal = 'obl'
    root = 'root'


class Producer(Enum):
    manual = 1
    computational = 2


class Query(ObjectType):

    dependency_enum = Field(DependencyEnum)
    producer = Field(Producer)

    def resolve_dependency_enum(root,info,dependency_enum):
        return dependency_enum
    
    def resolve_producer(root,info,producer):
        return producer


        