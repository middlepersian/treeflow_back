import requests
from django.core.cache import cache
from ..models import BibEntry

def only_cache(bibentry:BibEntry):
    """
    This function takes a BibEntry object and returns a dictionary of the
    corresponding entry in the Zotero database.
    """
    zotero_id = bibentry.key.upper()

    # check if the entry is in the cache
    zotero_entry = cache.get(zotero_id)
    if zotero_entry:
        return zotero_entry, True
    else:
        return None, False
    

def request_zotero_api_for_collection(group_key, collection_key):
    """ This function takes a group_key and a collection_key, checks the cache
    for the corresponding collection, and if not found, requests it from the
    Zotero API.
    """

    # check if the entry is in the cache
    zotero_collection = cache.get(collection_key)
    if zotero_collection:
        return zotero_collection, True
    
    # if not, request it from the Zotero API
    zotero_url = f"https://api.zotero.org/groups/{group_key}/collections/{collection_key}/items?sort=date&format=json&include=data,bib&linkwrap=0"
    try:
        r = requests.get(zotero_url)
        if r.ok:
            r = r.json()
            cache.set(collection_key, r)
        else:
            raise Exception(f"Request to Zotero API failed with status code {r.status_code}")
    except:
        r = None

    return r, False

def request_zotero_api_for_bibentry(bibentry:BibEntry):
    """
    This function takes a BibEntry object and returns a dictionary of the
    corresponding entry in the Zotero database.
    """
    zotero_id = bibentry.key.upper()

    # check if the entry is in the cache
    zotero_entry = cache.get(zotero_id)
    if zotero_entry:
        return zotero_entry, True
    
    # if not, request it from the Zotero API
    zotero_url = f"https://api.zotero.org/groups/2116388/items/{zotero_id}"
    try:
        r = requests.get(zotero_url)
        if r.ok:
            r = r.json()
            cache.set(zotero_id, r)
        else:
            raise Exception(f"Request to Zotero API failed with status code {r.status_code}")
    except:
        r = None

    return r, False

# request the whole collection and keep in cache. 