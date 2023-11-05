
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction

from treeflow.corpus.forms.token_form import TokenForm
from treeflow.corpus.models import Token

def update_token(request):
    if request.method == 'POST':
        token_id = request.POST.get('token_id')
        # Get the token object safely
        token = get_object_or_404(Token, id=token_id)
        
        # To avoid race conditions, consider using 'select_for_update' in a transaction.
        # This example assumes you're not using 'select_for_update' right now,
        # but it's included here for your reference.
        # with transaction.atomic():
        #     token = Token.objects.select_for_update().get(id=token_id)

        token_form = TokenForm(request.POST, instance=token)
        if token_form.is_valid():
            token_form.save()
            messages.success(request, 'Token updated successfully.')
        else:
            messages.error(request, 'Error updating token.')

        # Redirect to the same page to show the updated information
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('corpus:token_list')  # Replace 'corpus:token_list' with your appropriate URL name
