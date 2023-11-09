from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from treeflow.corpus.models.token import Token

def delete_token_view(request, token_id):
    if request.method == "POST":
        with transaction.atomic():
            # Capture current 'page' from the request before the transaction
            current_page = request.POST.get('page') or request.GET.get('page', 1)
            token_to_delete = get_object_or_404(Token.objects.select_for_update(), id=token_id)
            text_id = str(token_to_delete.text_id)  # Assuming token_to_delete has a 'text_id' attribute

            # Perform the delete operation
            Token.delete_token(token_to_delete.id)

            # Redirect back to the same page of 'tokens' view after deleting the token
            redirect_url = reverse('corpus:tokens') + f'?page={current_page}&text_id={text_id}'
            return HttpResponseRedirect(redirect_url)
    else:
        # Return a method not allowed response or redirect as needed
        return HttpResponse("Method not allowed", status=405)
