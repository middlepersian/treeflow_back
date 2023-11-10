from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from treeflow.corpus.forms.token_form import TokenForm
from treeflow.corpus.models import Token, POS
from treeflow.corpus.forms.pos_form import POSForm  # Make sure to create this form or import if already created

# Create a POSFormSet using the inlineformset_factory
POSFormSet = inlineformset_factory(Token, POS, form=POSForm, fields=('pos', 'type'), extra=1, can_delete=True)

def update_token(request, token_id=None):  # You can use token_id as a parameter if you want to
    token = get_object_or_404(Token, pk=token_id) if token_id else None

    if request.method == 'POST':
        token_form = TokenForm(request.POST, instance=token, token=token, prefix='token')
        pos_formset = POSFormSet(request.POST, instance=token, prefix='pos') if token else None

        # Check if both the token form and pos formset are valid
        if token_form.is_valid() and (pos_formset.is_valid() if pos_formset else True):
            saved_token = token_form.save()  # Save the token form and get the saved token instance

            if pos_formset:
                pos_formset.instance = saved_token  # Assign the saved token as the instance for the formset
                pos_formset.save()  # Save the formset to create/update/delete POS instances

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        token_form = TokenForm(instance=token, prefix='token')
        pos_formset = POSFormSet(instance=token, prefix='pos') if token else None

    # Pass both the token form and the pos formset to the template
    context = {
        'token_form': token_form,
        'pos_formset': pos_formset,
        'token_id': token_id
    }
    return render(request, 'update_token.html', context)
