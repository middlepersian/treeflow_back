from django.shortcuts import redirect, get_object_or_404
from  treeflow.corpus.models import Text

def dropdown_redirect(request):
    text_id = request.GET.get('text_id')
    target_view = request.GET.get('current_view')
    
    if text_id:
        # Ensure the text_id is valid and exists
        get_object_or_404(Text, id=text_id)

        if target_view:
            return redirect(target_view, text_id=text_id)
        else:
            # show errror message
            pass
    else:
        # show error message
        pass