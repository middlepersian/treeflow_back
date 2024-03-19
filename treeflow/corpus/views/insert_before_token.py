from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from treeflow.corpus.models.token import Token
from treeflow.corpus.models.section import Section

import logging
logger = logging.getLogger(__name__)

@login_required
def insert_before_token_view(request, token_id):
    if request.method == "POST":
        with transaction.atomic():
            current_page = request.POST.get('page', 1)
            source = request.POST.get('source', 'tokens')
            reference_token = get_object_or_404(Token.objects.select_for_update(), id=token_id)
            new_token_data = {}  # Populate with actual data as necessary
            
            # Insert the new token before the reference token
            new_token = Token.insert_before(reference_token.id, new_token_data, user=request.user)  # Pass the current user to the method
            
            # Log the source of the request and the newly created token
            logger.info(f"insert_before_token_view: source={source}, new_token_id={new_token.id}")
            
            text_id = str(reference_token.text_id)
            
            if source == 'sentences':
                # add the token to the sentence
                sentence_id = request.POST.get('sentence_id')
                sentence = get_object_or_404(Section.objects.select_for_update(), id=sentence_id)
                sentence.tokens.add(new_token)
                sentence.save()
                redirect_url = reverse('corpus:sentences', kwargs={'text_id': text_id}) + f'?page={current_page}#token-{new_token.id}'
            elif source == 'sentence': 
                # add the token to the sentence
                sentence_id = request.POST.get('sentence_id')
                sentence = get_object_or_404(Section.objects.select_for_update(), id=sentence_id)
                sentence.tokens.add(new_token)
                sentence.save()
                redirect_url = reverse('corpus:sentence', kwargs={'sentence_id': sentence_id}) 
            else:
                # Redirect to the tokens view by default
                redirect_url = reverse('corpus:tokens', kwargs={'text_id': text_id}) + f'?page={current_page}#token-{new_token.id}'

            return HttpResponseRedirect(redirect_url)
    else:
        # Return a method not allowed response if the request method is not POST
        logger.warning("Received a non-POST request for insert_before_token_view")
        return HttpResponse("Method not allowed", status=405)
