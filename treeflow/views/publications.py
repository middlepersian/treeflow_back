# views.py
from django.shortcuts import render
from django.core.cache import cache
from treeflow.datafeed.cache import update_zotero_data_in_cache  # Import the shared task

def zotero_view(request):
    publications = cache.get('zotero_publications')
    
    if not publications:
        update_zotero_data_in_cache()  

    publications = cache.get('zotero_publications', [])  # Attempt to fetch from cache again
    return render(request, 'pages/publications.html', {'publications': publications})
