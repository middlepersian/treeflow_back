from ..models import Section, Token, Text

import logging

from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from datetime import datetime

import csv

from django.http import StreamingHttpResponse, JsonResponse
from treeflow.datafeed.management.commands.export_text_mptf import text_to_mptf
from treeflow.datafeed.management.commands.export_text_conllu import text_to_conllu
# Set up logging
logger = logging.getLogger(__name__)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def resolve_state_mpft(request, text_id):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"status":"error","error": "User is not authenticated"})
    
    logger.debug(f"resolve_state_mpft: {text_id}")
    
    text = get_object_or_404(Text, id=text_id)
    text_cache_key = text.identifier+"_mpft"
    
    cached_data = cache.get(text_cache_key)
    logger.debug(f"resolve_state: {text_id} - {cached_data}")
    if not cached_data:
        cache.set(text_cache_key, {"status":"pending","data":[]})
        cached_data = cache.get(text_cache_key)
        text_to_mptf(text=text, cache_key=text_cache_key)
        return JsonResponse(cached_data)
    
    if cached_data["status"] == "pending":
        return JsonResponse(cached_data)
    
    return JsonResponse({"status":"success","data":[],})

def download_text_mpft(request, text_id):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"status":"error","error": "User is not authenticated"})
    
    logger.debug(f"download_text: {text_id}")
    text = get_object_or_404(Text, id=text_id)

    text_cache_key = text.identifier+"_mpft"
    cached_data = cache.get(text_cache_key)

    if not cached_data:
        # return error
        return JsonResponse({"status":"error","error": "Data not found"})
    if cached_data["status"] == "pending":
        # return error
        return JsonResponse({"status":"error","error": "Data is still being processed"})
    
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t')
    return StreamingHttpResponse(
        (writer.writerow(row) for row in cached_data["data"]),
        content_type="text/csv",
        headers={'Content-Disposition': f'attachment; filename="{text.identifier}_mptf.csv"'}
    )

def resolve_state_conllu(request, text_id):
 # check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"status":"error","error": "User is not authenticated"})
    
    logger.debug(f"resolve_state_conllu: {text_id}")
    
    text = get_object_or_404(Text, id=text_id)
    text_cache_key = text.identifier+"_conllu"
    
    cached_data = cache.get(text_cache_key)
    logger.debug(f"resolve_state: {text_id} - {cached_data}")
    if not cached_data:
        cache.set(text_cache_key, {"status":"pending","data":[]})
        cached_data = cache.get(text_cache_key)
        text_to_conllu(text=text, cache_key=text_cache_key)
        return JsonResponse(cached_data)
    
    if cached_data["status"] == "pending":
        return JsonResponse(cached_data)
    
    return JsonResponse({"status":"success","data":[],})

def download_text_conllu(request, text_id):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"status":"error","error": "User is not authenticated"})
    
    logger.debug(f"download_text: {text_id}")
    text = get_object_or_404(Text, id=text_id)

    text_cache_key = text.identifier+"_conllu"
    cached_data = cache.get(text_cache_key)

    if not cached_data:
        # return error
        return JsonResponse({"status":"error","error": "Data not found"})
    if cached_data["status"] == "pending":
        # return error
        return JsonResponse({"status":"error","error": "Data is still being processed"})
    
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t')
    return StreamingHttpResponse(
        (writer.writerow(row) for row in cached_data["data"]),
        content_type="text/csv",
        headers={'Content-Disposition': f'attachment; filename="{text.identifier}_conllu.csv"'}
    )