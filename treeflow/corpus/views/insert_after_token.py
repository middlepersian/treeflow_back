from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.db import transaction
from django.urls import reverse
from treeflow.corpus.models.token import Token
from treeflow.corpus.models.section import Section
import logging
logger = logging.getLogger(__name__)

def insert_after_token_view(request, token_id):
    if request.method == "POST":
        with transaction.atomic():
            # Capture current 'page' from the request before the transaction
            current_page = request.POST.get('page') or request.GET.get('page', 1)
            source = request.POST.get('source', 'tokens')  # Default to 'tokens' if not provided
            reference_token = get_object_or_404(Token.objects.select_for_update(), id=token_id)
            new_token_data = {}  # Populate with actual data as necessary
            new_token = Token.insert_after(reference_token.id, new_token_data)
            #log the source of the request
            logger.info(f"insert_after_token_view: source={source}")
            
            # Redirect back to the same page of 'tokens' view after inserting the token
            text_id = str(reference_token.text_id)  # Assuming reference_token has a 'text_id' attribute
            # Determine the redirect URL based on the source
            if source == 'sentences':
                # add the token to the sentence
                sentence_id = request.POST.get('sentence_id')
                sentence = get_object_or_404(Section.objects.select_for_update(), id=sentence_id)
                sentence.tokens.add(new_token)
                sentence.save()
                redirect_url = reverse('corpus:sentences', kwargs={'text_id': text_id}) + f'?page={current_page}#token-{new_token.id}'
            if source == 'sentence': 
                # add the token to the sentence
                sentence_id = request.POST.get('sentence_id')
                sentence = get_object_or_404(Section.objects.select_for_update(), id=sentence_id)
                sentence.tokens.add(new_token)
                sentence.save()
                redirect_url = reverse('corpus:sentence', kwargs={'sentence_id': sentence_id}) 
            else:
                redirect_url = reverse('corpus:tokens', kwargs={'text_id': text_id}) + f'?page={current_page}#token-{new_token.id}'


            return HttpResponseRedirect(redirect_url)
    else:
        # Return a method not allowed response or redirect as needed
        return HttpResponse("Method not allowed", status=405)
