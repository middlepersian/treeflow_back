# views.py
from django.shortcuts import render
from django.core.cache import cache
from treeflow.datafeed.tasks import update_zotero_data_in_cache  # Import the shared task

def zotero_view(request):
    publications = cache.get('zotero_publications')
    
    if not publications:
        update_zotero_data_in_cache.apply()  # Call the task to update cache
        # Optionally, wait for the task to complete and then fetch from cache
        # or handle the waiting period appropriately in your view

    publications = cache.get('zotero_publications', [])  # Attempt to fetch from cache again
    return render(request, 'pages/publications.html', {'publications': publications})
