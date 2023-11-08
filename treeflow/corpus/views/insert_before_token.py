from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.db import transaction
from treeflow.corpus.models.token import Token


def insert_before_token_view(request, token_id):
    if request.method == "POST":
        # Wrap operations in a transaction to ensure atomicity
        with transaction.atomic():
            # Fetch and lock the reference token to prevent concurrent modifications
            reference_token = get_object_or_404(
                Token.objects.select_for_update(), id=token_id)

            # Since you mentioned no additional data is needed, we can keep it empty or
            # include any defaults that your Token model may require
            new_token_data = {}

            # Use the class method 'insert_before' to create the new token
            new_token = Token.insert_before(reference_token.id, new_token_data)

            # Redirect or respond according to your application's needs after successful insertion
            return HttpResponse("New token inserted before token with ID: {}".format(token_id), status=200)
    else:
        return HttpResponse("Invalid request method.", status=405)
