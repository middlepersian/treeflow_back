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