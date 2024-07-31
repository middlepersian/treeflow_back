import logging

from django.db.models import Q, QuerySet
from django.shortcuts import render

from treeflow.corpus.models import Section, SectionToken, Token

logger = logging.getLogger(__name__)

def search_index(request):
    return render(request, "search-update-index.html")

def handle_search(request):
    request_data = request.GET
    query = request_data.get("query", "")

    if not query:
        return Section.objects.none()
    
    