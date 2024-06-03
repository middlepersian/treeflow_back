from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from treeflow.corpus.forms.section_token_form import SectionTokenForm
from treeflow.corpus.models import Token, SectionToken

def update_section_token_view(request, token_id):
    token = get_object_or_404(Token, id=token_id)
    section_token, created = SectionToken.objects.get_or_create(token=token)
    if request.method == 'POST':
        form = SectionTokenForm(request.POST, instance=section_token)
        if form.is_valid():
            section_token = form.save(commit=False)
            section_token.token = token
            section_token.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SectionTokenForm(instance=section_token)
    return render(request, 'section_token_form.html', {'form': form, 'token': token})
