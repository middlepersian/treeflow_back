from django.shortcuts import render
from treeflow.corpus.models import Text

def texts_view(request):
    # Get all text instances
    texts = Text.objects.all()
    # Render the template with the texts context
    return render(request, 'texts.html', {'texts': texts})
