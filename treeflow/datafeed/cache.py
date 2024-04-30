from django.core.cache import cache
from django.db.models import Prefetch
from django.db.models import Count
from treeflow.corpus.models import Text, Section, Token, Source
from treeflow.dict.models import Lemma
from treeflow.images.models import Image
from treeflow.corpus.utils.zotero import request_zotero_api_for_collection
import logging

logger = logging.getLogger(__name__)

def cache_all_zotero_sources():
    logger.debug("Running cache_all_zotero_sources task")

    group_key = "2116388"
    collection_key = "2CGA8RXR"

    zotero_data, _ = request_zotero_api_for_collection(group_key, collection_key)

    cache_key = 'zotero_sources'
    current_cache = cache.get(cache_key)

    if not current_cache:
        logger.info("Cache miss for sources - Sources have been updated in the cache.")
        cache.set(cache_key, zotero_data, timeout=None) # Set no timeout
    else:
        logger.info("Cache hit for sources - Sources have not been updated in the cache.")
        cache.set(cache_key, current_cache, timeout=None)  # Set no timeout

def update_zotero_data_in_cache():
    logger.debug("Running update_zotero_data_in_cache task")

    collection_keys = {
    "Preliminary Publications": "4DBIWSQG",
    "Project Publications": "B3BHZEGW",
    "Related Publications": "8VFMBB74",
    "Presentations": "YZX3G3DF",
    "Related Presentations": "2DNQXANE",
    }

    publications = {
        'group_key': 2116388,
        'collections' : []
    }

    for key, value in collection_keys.items():
        zotero_data, _ = request_zotero_api_for_collection(publications["group_key"], value)
        publications["collections"].append({"name": key, "data": zotero_data})

    cache_key = 'zotero_publications'
    current_cache = cache.get(cache_key)

    if not current_cache:
        logger.info("Cache miss for publications - Publications have been updated in the cache.")
        cache.set(cache_key, publications['collections'], timeout=None) # Set no timeout
    else:
        logger.info("Cache hit for publications - Publications have not been updated in the cache.")
        cache.set(cache_key, current_cache, timeout=None)  # Set no timeout


def cache_all_texts():
    logger.info("Running cache_all_texts task")
    cache_key_texts = "all_texts"
    current_cache = cache.get(cache_key_texts)

    if not current_cache:
        texts = Text.objects.annotate(token_count=Count('token_text')).order_by('identifier')
        cache.set(cache_key_texts,  texts, timeout=None)  # Set no timeout
        logger.info("Cache miss fortexts - Texts have been updated in the cache.")
    else:
        logger.info("Cache hit for texts - Texts have not been updated in the cache.")
        cache.set(cache_key_texts, current_cache, timeout=None)


def cache_sections_for_texts():
    logger.info("Starting cache_sections_for_texts task")
    
    # Call cache_all_texts to ensure texts are cached
    cache_all_texts()

    # Since cache_all_texts ensures that all texts are cached under the key "all_texts",
    # we can retrieve the cached texts directly.
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)
    
    # Proceed with caching sections for each text
    for text in texts:
        cache_key = f"sections_for_text_{text.id}"
        all_sections = Section.objects.filter(text=text)
        sentence_ids = list(all_sections.filter(type='sentence').values_list('id', flat=True))
        section_types = set(all_sections.exclude(type='sentence').values_list('type', flat=True).distinct())        
        cache.set(cache_key, {
            'sentence_ids': sentence_ids,  
            'section_types': section_types,
        })
        logger.info(f"Sections cached for text: {text.id}")

def cache_manuscripts():
    logger.info("Starting cache_manuscripts task")
    cache_key_manuscripts = "manuscripts"
    
    logger.info("Fetching manuscripts from database.")
    manuscripts = Source.objects.filter(type="manuscript").order_by("identifier")
    
    logger.info("Manuscripts cached")
    cache.set(cache_key_manuscripts, manuscripts)


def cache_images(): 
    logger.info("Starting cache_images task")
    cache_key_images = "images"
    images = Image.objects.select_related('source')
    cache.set(cache_key_images, images)
    logger.info("Images cached")

    
def cache_lemmas():
    logger.info("Starting cache_lemmas task")
    cache_key_lemmas = "lemmas"
    lemmas = Lemma.objects.only('id', 'word')
    cache.set(cache_key_lemmas, lemmas)
    logger.info("Lemmas cached")