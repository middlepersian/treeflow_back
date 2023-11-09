# views.py
from django.shortcuts import redirect, render, get_object_or_404
from treeflow.corpus.forms.token_form import TokenForm
from treeflow.corpus.models import Token

def update_token(request):
    if request.method == 'POST':
        token_id = request.POST.get('token_id')
        token = get_object_or_404(Token, pk=token_id)
        # Pass 'token' as a keyword argument to TokenForm
        token_form = TokenForm(request.POST, instance=token, token=token)

        if token_form.is_valid():
            token_form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            # Handle the invalid form case
            return render(request, 'update_token.html', {'form': token_form, 'token_id': token_id})
    else:
        # Initialize the form for a GET request with 'token' if available
        token_id = request.GET.get('token_id')
        token = None
        if token_id:
            token = get_object_or_404(Token, pk=token_id)
        token_form = TokenForm(token=token) if token else TokenForm()
        return render(request, 'update_token.html', {'form': token_form, 'token_id': token_id})
