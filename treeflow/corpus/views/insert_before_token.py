from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.db import transaction
from django.urls import reverse
from treeflow.corpus.models.token import Token

def insert_before_token_view(request, token_id):
    if request.method == "POST":
        with transaction.atomic():
            # Capture current 'page' from the request before the transaction
            current_page = request.POST.get('page') or request.GET.get('page', 1)
            reference_token = get_object_or_404(Token.objects.select_for_update(), id=token_id)
            new_token_data = {}  # Populate with actual data as necessary
            new_token = Token.insert_before(reference_token.id, new_token_data)
            
            # Redirect back to the same page of 'tokens' view after inserting the token
            text_id = str(reference_token.text_id)  # Assuming reference_token has a 'text_id' attribute
            redirect_url = reverse('corpus:tokens') + f'?page={current_page}&text_id={text_id}'
            return HttpResponseRedirect(redirect_url)
    else:
        # Return a method not allowed response or redirect as needed
        return HttpResponse("Method not allowed", status=405)