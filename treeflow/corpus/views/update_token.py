# views.py
from django.shortcuts import redirect
from treeflow.corpus.forms.token_form import TokenForm
from treeflow.corpus.models import Token
def update_token(request):
    # Initialize the form with no instance
    token_form = None

    # Handle the form submission
    if request.method == 'POST':
        # Get the token ID from the posted form data
        token_id = request.POST.get('token_id')
        # Get the token instance associated with the token ID
        token = get_object_or_404(Token, pk=token_id)
        # Create a form instance with the POST data and the specific token instance
        token_form = TokenForm(request.POST, instance=token)

        if token_form.is_valid():
            # Save the form and thus the token with new data
            token_form.save()
            # Redirect to the same page to show the updated information
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

