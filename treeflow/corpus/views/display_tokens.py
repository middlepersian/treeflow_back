from django.shortcuts import render
from treeflow.corpus.models import Token
import uuid

def display_tokens_view(request):
    token_ids_str = request.GET.get('tokens', '')
    token_uuids = [uuid.UUID(token_id) for token_id in token_ids_str.split(',') if token_id]
    tokens = Token.objects.filter(id__in=token_uuids)
    return render(request, 'display_tokens.html', {'tokens': tokens})
