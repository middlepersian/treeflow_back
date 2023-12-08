from typing import Any
from ..models import BibEntry
from ..utils.zotero import request_zotero_api_for_bibentry, only_cache

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

class BibEntryListView(ListView):
    model = BibEntry
    template_name = 'bibentry_list.html'
    context_object_name = 'bibentries'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Iterate over each BibEntry and fetch Zotero data
        zotero_entries = []
        for bibentry in context['bibentries']:
            zotero_entry, from_cache = only_cache(bibentry)
            zotero_entries.append({
                'bibentry': bibentry,
                'zotero_entry': zotero_entry,
                'from_cache': from_cache,
            })

        context['zotero_entries'] = zotero_entries

        return context

    
class BibEntryDetailView(DetailView):
    model = BibEntry
    template_name = 'bibentry_detail.html'
    context_object_name = 'bibentry'
    pk_url_kwarg = 'bibEntry_id'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data from Zotero API
        zotero_entry, from_Cache = request_zotero_api_for_bibentry(self.object)

        if not zotero_entry or 'error' in zotero_entry:
            # Handle error case
            zotero_entry = {'error': 'Could not retrieve entry from Zotero API.'}
        context['zotero_entry'] = zotero_entry
        context['from_Cache'] = from_Cache

        # Modify the key in the BibEntry
        context['bibentry'].key = context['bibentry'].key.upper()

        return context
