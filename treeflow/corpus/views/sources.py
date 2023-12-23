from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import forms
from django.views.generic.edit import FormView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from ..forms import SourceForm, BibEntryForm

from ..enums.deprel_enum import Deprel
from treeflow.corpus.models import (
    BibEntry,
    Source
) 

import logging

from treeflow.images.models import Image

# Set up logging
logger = logging.getLogger(__name__)

# create a generic detail view for source
class SourceDetailView(DetailView):
    model = Source
    template_name = 'source_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Source'
        return context
    
# create a generic table view for source
class SourceTableView(ListView):
    model = Source
    fields = '__all__'
    template_name = 'source_table.html'
    context_object_name = 'sources'
    
    # get the queryset
    def get_queryset(self):
        qs1 = Source.objects.all().order_by('identifier').prefetch_related('references', 'sources')
        return qs1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Source'
        return context
    
# create a generic create view for source
class SourceCreateView(CreateView):
    model = Source
    fields = '__all__'  # Or specify the fields you want to include in the form
    template_name = 'source_create.html'  # Specify the template for the create view
    success_url = '/corpus/sources'  # Specify the URL to redirect to after successful creation
    
# create a generic update view for source
class SourceUpdateView(UpdateView):
    model = Source
    template_name = 'source_update.html'  # Specify the template for the create view
    success_url = '/corpus/sources'  # Specify the URL to redirect to after successful creation
    pk_url_kwarg = 'source_id'
    # add the form
    form_class = SourceForm
    
# create a generic delete view for source
class SourceDeleteView(DeleteView):
    model = Source
    template_name = 'source_delete.html'
    success_url = '/corpus/sources'
    pk_url_kwarg = 'source_id'



def create_source(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do something else
            return redirect('/corpus/sources/')
    else:
        form = SourceForm()

    return render(request, 'source_create.html', {'form': form})


def source_manuscripts(request):
    # get all sources that are manuscripts
    images = Image.objects.all().prefetch_related('source')

    #setup paginator
    paginator = Paginator(images, 50)
    page_number = request.GET.get('page')
    images_page = paginator.get_page(page_number)
    logger.debug('images_page: %s', images_page)
    context = {
        'manuscripts': images_page,
        'page_title': 'Manuscripts',
        
    }

    return render(request, 'source_manuscripts.html',context)

def add_related_source(request,source_id):
    source = get_object_or_404(Source, id=source_id)

    if request.method == 'POST':
        # Handle the form submission here if needed
        # You can manually update the sources based on the request data
        selected_sources_ids = request.POST.getlist('sources')
        source.sources.set(selected_sources_ids)
        source.save()
        return redirect('/corpus/sources/')  # Redirect to a success page

    available_sources = Source.objects.exclude(id=source_id)
    return render(request, 'source_related_source.html', {'source': source, 'available_sources': available_sources})

def add_related_bib(request,source_id):
    source = get_object_or_404(Source, id=source_id)
    bibs = BibEntry.objects.filter(source_references=source_id)
    if request.method == 'POST':
        # Check which form is submitted based on the button name or any other identifier
        if 'add_new' in request.POST:
            # Handle the form for adding a new BibEntry
            logger.debug('add_new')
            bib_form = BibEntryForm(request.POST)
            if bib_form.is_valid():
                new_bib_entry = bib_form.save(commit=False)
                new_bib_entry.save()
                source.references.add(new_bib_entry)
                source.save()
                return redirect('corpus:sources')

        elif 'add_existing' in request.POST:
            # Handle the form for adding an existing BibEntry
            selected_bibs_ids = request.POST.getlist('bibs')
            source.references.set(selected_bibs_ids)
            source.save()
            return redirect('corpus:sources')

    
    bib_form = BibEntryForm
    available_bibs = BibEntry.objects.all()
    
    return render(request, 'source_related_bibentry.html', {'source': source,'bib_form': bib_form, 'available_bibs': available_bibs, 'bibs': bibs})