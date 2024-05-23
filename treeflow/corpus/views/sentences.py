import logging
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render
from treeflow.corpus.models import Section, Token, Text, Source

logger = logging.getLogger(__name__)

def cache_manuscripts():
    cache_key = "manuscripts"
    manuscripts = cache.get(cache_key)
    if manuscripts is None:
        logger.info("Cache miss for manuscripts - Fetching from database.")
        manuscripts = Source.objects.filter(type="manuscript").order_by("identifier")
        cache.set(cache_key, manuscripts, timeout=3600)  # Cache for 1 hour
        logger.info("Manuscripts cached")
    else:
        logger.info("Manuscripts already cached")
    return manuscripts

def get_texts():
    return cache.get_or_set("all_texts", lambda: Text.objects.all(), timeout=3600)  # Cache for 1 hour

def get_sentences(text_id, page_number, items_per_page):
    token_prefetch = Prefetch(
        "tokens",
        queryset=Token.objects.select_related("image").prefetch_related(
            "lemmas", "senses", "pos_token", "feature_token", "comment_token"
        ),
        to_attr="tokens_list"
    )

    logger.info("Fetching sentences for text ID: %s", text_id)
    sentences = Section.objects.filter(type="sentence", text=text_id).prefetch_related(token_prefetch)
    paginator = Paginator(sentences, items_per_page)
    page_obj = paginator.get_page(page_number)
    logger.info("Number of sentences on current page: %d", len(page_obj))  # Log count after pagination
    return page_obj

@login_required
def sentences_view(request, text_id=None):
    manuscripts = cache_manuscripts()
    texts = get_texts()
    selected_text_id = text_id if text_id else request.GET.get("text_id")
    page_number = request.GET.get("page", 1)
    items_per_page = 10

    context = {
        "manuscripts": manuscripts,
        "texts": texts,
        "selected_text_id": selected_text_id or "",
        "current_view": "corpus:sentences",
    }

    if selected_text_id:
        page_obj = get_sentences(selected_text_id, page_number, items_per_page)
        context["page_obj"] = page_obj
    else:
        context["page_obj"] = Paginator(Section.objects.none(), items_per_page).get_page(1)
        logger.info("No text ID selected, providing empty paginator.")

    logger.info("Rendering sentences.html for text ID: %s", selected_text_id)
    return render(request, "sentences.html", context)