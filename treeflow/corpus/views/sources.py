from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import forms
from django.views.generic.edit import FormView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ..forms import SourceForm

from ..enums.deprel_enum import Deprel
from treeflow.corpus.models import (
    BibEntry,
    Source
) 

from treeflow.images.models import Image

    
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
    else:
        form = SourceForm()

    return render(request, 'source_create.html', {'form': form})


def source_manuscripts(request):
    # get all sources that are manuscripts
    images = Image.objects.all().prefetch_related('source')
    paginator = Paginator(images, 50)
    page_number = request.GET.get('page')
    images_page = paginator.get_page(page_number)
    context = {
        'images': images,
        'page_obj': images_page,
        'page_title': 'Manuscripts',
        
    }

    return render(request, 'source_manuscripts.html', {'manuscripts': images})

