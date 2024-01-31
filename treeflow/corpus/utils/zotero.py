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
            #cache.set(collection_key, r)
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

# request a list of entries from the collection and keep in cache.
def request_zotero_for_list(bibentries:list[BibEntry]):
    """
    This function takes a list of BibEntry objects and returns a list of
    dictionaries of the corresponding entries in the Zotero database.
    """
    zotero_ids = [bibentry.key.upper() for bibentry in bibentries]

    # check if the entries are in the cache
    zotero_entries = cache.get_many(zotero_ids)
    if len(zotero_entries) == len(zotero_ids):
        return zotero_entries, True
    
    # check which entries are missing from the cache
    zotero_ids = [zotero_id for zotero_id in zotero_ids if zotero_id not in zotero_entries.keys()]

    # if not for all entries, request them from the Zotero API

    
    # if not, request them from the Zotero API
    zotero_url = f"https://api.zotero.org/groups/2116388/items?itemKey={','.join(zotero_ids)}"
    try:
        r = requests.get(zotero_url)
        if r.ok:
            r = r.json()
            for entry in r:
                cache.set(entry['data']['key'], entry)
        else:
            raise Exception(f"Request to Zotero API failed with status code {r.status_code}")
    except:
        r = None

    return r, False