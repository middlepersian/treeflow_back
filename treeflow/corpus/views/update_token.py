# views.py
from django.shortcuts import redirect
from treeflow.corpus.forms.token_form import TokenForm
from treeflow.corpus.models import Token

def update_token(request):
    if request.method == 'POST':
        token_id = request.POST.get('token_id')
        token_form = TokenForm(request.POST, instance=Token.objects.get(id=token_id))
        if token_form.is_valid():
            token_form.save()
            # Redirect to the same page to show the updated information
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
