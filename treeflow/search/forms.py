from django.forms import modelformset_factory
from .models import SearchCriteria


SearchFormSet = modelformset_factory(
    SearchCriteria, fields=(
        "query_type",
        "query_field",
        "query_value",
        "pos_token",
        "remove_stopwords",
        "distance",
        "feature",
        "feature_value",
        "lemma_language",
        "lemma_value",
        "meaning_language",
        "meaning_value",
    )
)
