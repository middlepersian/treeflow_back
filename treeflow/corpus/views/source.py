from django.shortcuts import render, get_object_or_404
from ..models.bibliography import BibEntry
from ..models.source import Source

def source_list(request):
    sources = Source.objects.all()
    return render(request, 'corpus/source_list.html', {'sources': sources})

def source_detail(request, pk):
    source = get_object_or_404(Source, pk=pk)
    return render(request, 'corpus/source_detail.html', {'source': source})

def bibenty_list(request):
    bibenties = BibEntry.objects.all()
    return render(request, 'corpus/bibenty_list.html', {'bibenties': bibenties})

def bibenty_detail(request, pk):
    bibenty = get_object_or_404(BibEntry, pk=pk)
    return render(request, 'corpus/bibenty_detail.html', {'bibenty': bibenty})
