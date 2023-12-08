from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from treeflow.corpus.forms.text_form import TextForm
from treeflow.corpus.models import Text
import logging

logger = logging.getLogger(__name__)    
def texts_view(request):
    texts = Text.objects.all()
    logger.debug("request method: %s", request.method)

    if request.method == 'POST':
        text_id = request.POST.get('text_id')
        logger.debug("text_id: %s", text_id)
        if text_id:
            text = get_object_or_404(Text, pk=text_id)
            form = TextForm(request.POST, instance=text)
        else:
            form = TextForm(request.POST)

        if form.is_valid():
            saved_text = form.save()
            if request.headers.get('HX-Request'):  # Check if it's an HTMX request
                html = render_to_string('text_row.html', {'text': saved_text})
                return JsonResponse({'html': html})
            # Redirect for non-HTMX request
        else:
            # Handle form errors here (especially for HTMX response)
            pass

    else:
        form = TextForm()

    context = {'texts': texts, 'form': form}
    return render(request, 'texts.html', context)
