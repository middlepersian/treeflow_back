from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from treeflow.corpus.models import POS

@require_POST
@login_required
def update_pos_ajax(request):
    data = json.loads(request.body)
    token_id = data.get('token_id')  # Get the Token ID from the AJAX request
    pos_id = data.get('pos_id')
    new_pos_value = data.get('new_pos_value')

    # Check if the POS belongs to the correct Token before updating
    try:
        pos_instance = POS.objects.get(pk=pos_id, token_id=token_id)  # Filter by Token ID as well
        pos_instance.pos = new_pos_value.upper()
        pos_instance.save()
        return JsonResponse({'status': 'success'})
    except POS.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'POS not found or does not belong to the specified Token'}, status=404)
